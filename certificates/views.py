from django.shortcuts import render
from django.http import HttpResponse
from .models import Participant
from django.conf import settings
from PIL import Image, ImageDraw, ImageFont
import os


def home(request):
    return render(request, 'index.html')


def verify_page(request):
    context = {}

    if request.method == "POST":
        email = request.POST.get("email")
        name = request.POST.get("name")

        try:
            participant = Participant.objects.get(email=email)
            context["email"] = email
            context["participant"] = participant

            # Certificate already generated → everything locked
            if participant.certificate_generated:
                context["name_locked"] = True
                context["already_generated"] = True
                return render(request, "verify.html", context)

            # If user submitted a name (editing or first time)
            if name:
                clean_name = name.strip()

                if len(clean_name) < 3:
                    context["error"] = "Please enter a valid name."
                    context["email_valid"] = True
                    return render(request, "verify.html", context)

                participant.name = clean_name.title()
                participant.save()
                context["name_locked"] = True

            else:
                # Just email verified, show name field (pre-filled)
                context["email_valid"] = True

        except Participant.DoesNotExist:
            context["error"] = "Email not registered"

    return render(request, "verify.html", context)


def generate_certificate(request):
    if request.method == "POST":
        email = request.POST.get("email")

        try:
            participant = Participant.objects.get(email=email)
        except Participant.DoesNotExist:
            return HttpResponse("Participant not found.", status=404)

        if not participant.name:
            return HttpResponse("Please verify your name first.")

        # Static paths
        static_root = os.path.join(settings.BASE_DIR, 'certificates', 'static')

        if participant.position in ["top3", "top10"]:
            template_path = os.path.join(static_root, "certificates", "top10.png")
        else:
            template_path = os.path.join(static_root, "certificates", "participant.png")

        font_path = os.path.join(static_root, "fonts", "Poppins-Bold.ttf")

        img = Image.open(template_path)
        draw = ImageDraw.Draw(img)
        name = participant.name.upper()

        # ---------- AUTO FONT RESIZE ----------
        font_size = 48
        max_width = img.width * 0.60
        font = ImageFont.truetype(font_path, font_size)

        while font_size > 30:
            bbox = draw.textbbox((0, 0), name, font=font)
            text_width = bbox[2] - bbox[0]
            if text_width <= max_width:
                break
            font_size -= 2
            font = ImageFont.truetype(font_path, font_size)

        # ---------- FINAL NAME POSITION (LOCKED TO DESIGN) ----------
        bbox = draw.textbbox((0, 0), name, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        # Perfect horizontal center
        x = (img.width - text_width) / 2 - bbox[0]

        # 🔥 Correct vertical position for name on this certificate
        name_center_y = 545

        y = name_center_y - (text_height / 2) - bbox[1]

        draw.text((x, y), name, fill="black", font=font)

        # Mark as generated
        if not participant.certificate_generated:
            participant.certificate_generated = True
            participant.save()

        response = HttpResponse(content_type="image/png")
        response['Content-Disposition'] = f'attachment; filename="{name}_certificate.png"'
        img.save(response, "PNG")

        return response
