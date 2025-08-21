from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings

from .models import Resume
from .utils import (
    extract_text_from_pdf,
    extract_text_from_docx,
    extract_email_from_text,
    extract_skills,
    calculate_score
)

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('upload')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')


from .models import JobDescription

@login_required
def upload_files(request):
    if request.method == 'POST':
        jd_text = request.POST.get('jd_text', '').strip()
        jd_file = request.FILES.get('jd_file')

        if not jd_text and jd_file:
            if jd_file.name.lower().endswith('.pdf'):
                jd_text = extract_text_from_pdf(jd_file)
            elif jd_file.name.lower().endswith('.docx'):
                jd_text = extract_text_from_docx(jd_file)

        if not jd_text:
            messages.error(request, "Please provide a job description.")
            return redirect('upload')

        # First, create the JobDescription instance
        job_desc = JobDescription.objects.create(
            content=jd_text
        )

        top_n = int(request.POST.get('top_n', 3))
        uploads = request.FILES.getlist('resumes')
        scored = []

        jd_skills = extract_skills(jd_text)

        for f in uploads:
            ext = f.name.lower().split('.')[-1]
            if ext == 'pdf':
                txt = extract_text_from_pdf(f)
            elif ext == 'docx':
                txt = extract_text_from_docx(f)
            else:
                continue

            email = extract_email_from_text(txt) or "N/A"
            score = calculate_score(jd_text, txt)
            resume_skills = extract_skills(txt)
            missing_skills = jd_skills - resume_skills

            # Link resume to the JobDescription
            r = Resume.objects.create(
                file=f,
                content=txt,
                email=email,
                score=score,
                job_description=job_desc  # ✅ important
            )
            r.missing_skills = list(missing_skills)
            r.matching_skills = list(resume_skills & jd_skills)
            scored.append(r)

        scored.sort(key=lambda x: x.score, reverse=True)
        top_resumes = scored[:top_n]

        request.session['current_upload_ids'] = [r.id for r in scored]
        request.session['top_ids'] = [r.id for r in top_resumes]

        return render(request, 'results.html', {
            'resumes': scored,
            'top_resumes': top_resumes,
            'top_resume_ids': [r.id for r in top_resumes],
        })

    return render(request, 'upload.html')

@login_required
def send_selected(request):
    if request.method == 'POST':
        current_ids = request.session.get('current_upload_ids', [])
        top_ids = request.session.get('top_ids', [])

        current_resumes = Resume.objects.filter(id__in=current_ids)
        top_resumes = Resume.objects.filter(id__in=top_ids)

        # ✅ Selected = system-determined top resumes
        selected_resumes = top_resumes  

        sent_count = 0
        for r in selected_resumes:
            if r.email and r.email != "N/A":
                try:
                    send_mail(
                        subject="🎉 You’re Shortlisted!",
                        message="Hello! We are happy to announce that you are going to be a part of our organization.\n\n"
                                "Congrats! We will connect with you soon.",
                        from_email=settings.EMAIL_HOST_USER,
                        recipient_list=[r.email],
                        fail_silently=False
                    )
                    sent_count += 1
                except Exception as e:
                    print(f"Error sending email to {r.email}: {e}")

        message = f"✅ Emails sent to {sent_count} selected candidate(s)!"
        return render(request, 'results.html', {
            'message': message,
            'resumes': current_resumes,
            'top_resumes': top_resumes,
            'top_resume_ids': top_ids
        })


@login_required
def send_rejected(request):
    if request.method == 'POST':
        current_ids = request.session.get('current_upload_ids', [])
        top_ids = request.session.get('top_ids', [])

        current_resumes = Resume.objects.filter(id__in=current_ids)
        top_resumes = Resume.objects.filter(id__in=top_ids)

        # ✅ Rejected = current resumes not in top_ids
        rejected_resumes = [r for r in current_resumes if r.id not in top_ids]

        sent_count = 0
        for r in rejected_resumes:
            if r.email and r.email != "N/A":
                msg = (
                    "Hello! We are sorry to inform you that you were not selected for the position.\n"
                    "Thank you for applying. Please try again later.\n"
                )
                try:
                    send_mail(
                        subject="❌ Application Status",
                        message=msg,
                        from_email=settings.EMAIL_HOST_USER,
                        recipient_list=[r.email],
                        fail_silently=False
                    )
                    sent_count += 1
                except Exception as e:
                    print(f"Error sending email to {r.email}: {e}")

        message = f"❌ Emails sent to {sent_count} rejected candidate(s)!"
        return render(request, 'results.html', {
            'message': message,
            'resumes': current_resumes,
            'top_resumes': top_resumes,
            'top_resume_ids': top_ids
        })

