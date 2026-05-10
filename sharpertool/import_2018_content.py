"""One-shot: restore HomePage + ResumePage content from the 2018-07-09
production pg_dump that the user fortunately kept around.

Run with:
    DJANGO_SETTINGS_MODULE=sharpertool.settings.dev SECRET_KEY=local-dev-key \\
    DATABASE_URL=sqlite:///$(pwd)/sharpertool/db.sqlite3 \\
    DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1 \\
    .venv/bin/python sharpertool/manage.py shell < sharpertool/import_2018_content.py

Skips image FKs (sets to None) — the original Image rows are not in the
sqlite, only the files on disk under media/. Wire those up later through
the admin or a follow-up import.
"""
import json

from home.models import HomePage, HomePageHighlight
from resume.models import (
    ResumePage,
    ResumeProjectItem,
    EducationItem,
    Skills,
    Experience,
    ResumeBlog,
)

with open("/tmp/import_content.json") as f:
    data = json.load(f)

home_data = data["home"]
resume_data = data["resume"]

# --- HomePage ---
home = HomePage.objects.get(slug="home")
home.tagline = home_data["tagline"]
home.title = home_data["title"]
home.draft_title = home_data.get("draft_title", home_data["title"])
home.save()

home.highlights.all().delete()
for h in home_data["highlights"]:
    HomePageHighlight.objects.create(
        page=home,
        sort_order=h.get("sort_order"),
        name=h["name"],
        link=h["link"],
        text=h["text"],
    )
home.save_revision().publish()
print(f"HomePage: tagline={home.tagline!r}, highlights={home.highlights.count()}")

# --- ResumePage ---
ResumePage.objects.filter(slug__in=["resume", "resume-ed-henderson"]).delete()
resume = ResumePage(
    title=resume_data["title"],
    slug=resume_data["slug"],
    seo_title=resume_data.get("seo_title", ""),
    show_in_menus=resume_data.get("show_in_menus", True),
    heading=resume_data["heading"],
    intro=resume_data["intro"],
    name=resume_data["name"],
    dob=resume_data.get("dob") or "",
    email=resume_data.get("email") or "",
    address=resume_data.get("address") or "",
    website=resume_data.get("website"),
    phone=resume_data.get("phone") or "",
    contact_info=resume_data.get("contact_info") or "",
    contact_email=resume_data.get("contact_email"),
    contact_longitude=resume_data.get("contact_longitude"),
    contact_latitude=resume_data.get("contact_latitude"),
)
home.add_child(instance=resume)
resume.save_revision().publish()

for item in resume_data["project_item"]:
    ResumeProjectItem.objects.create(
        page=resume,
        sort_order=item.get("sort_order"),
        section=item.get("section"),
        title=item["title"],
        subtext=item.get("subtext") or "",
    )
for item in resume_data["education"]:
    EducationItem.objects.create(
        page=resume,
        sort_order=item.get("sort_order"),
        title=item["title"],
        start=item.get("start") or "",
        end=item.get("end") or "",
        text=item.get("text") or "",
    )
for item in resume_data["skills"]:
    Skills.objects.create(
        page=resume,
        sort_order=item.get("sort_order"),
        title=item["title"],
        percent=item.get("percent") or "",
    )
for item in resume_data["experience"]:
    Experience.objects.create(
        page=resume,
        sort_order=item.get("sort_order"),
        title=item["title"],
        start=item.get("start") or "",
        end=item.get("end") or "",
        text=item.get("text") or "",
    )
for item in resume_data["blog_entries"]:
    ResumeBlog.objects.create(
        page=resume,
        sort_order=item.get("sort_order"),
        title=item["title"],
        text=item.get("text") or "",
    )

resume.save_revision().publish()
print(
    f"ResumePage: name={resume.name!r}, "
    f"projects={resume.project_item.count()}, "
    f"education={resume.education.count()}, "
    f"skills={resume.skills.count()}, "
    f"experience={resume.experience.count()}, "
    f"blog_entries={resume.blog_entries.count()}"
)
