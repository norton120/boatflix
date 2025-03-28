from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
from webapp.persist import Compose
from typing import Optional

router = APIRouter(prefix="/web")

# Set up templates directory
templates = Jinja2Templates(directory=str(Path(__file__).parent / "templates"))

def get_service_image(service_name: str) -> Optional[str]:
    """Check if a service has a corresponding image in the assets/services directory."""
    image_path = Path(__file__).parent / "assets" / "services" / f"{service_name.lower()}.png"
    if image_path.exists():
        return f"/assets/services/{service_name.lower()}.png"
    # Check for SVG as fallback
    svg_path = Path(__file__).parent / "assets" / "services" / f"{service_name.lower()}.svg"
    if svg_path.exists():
        return f"/assets/services/{service_name.lower()}.svg"
    return None

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    compose = Compose()
    # Filter out the webapp service and add image paths
    services = []
    for s in compose.services:
        if s.name != "webapp":
            s.image_path = get_service_image(s.name)
            services.append(s)
    return templates.TemplateResponse(
        "home.html",
        {"request": request, "title": "Home", "services": services}
    )

@router.get("/service/{service_name}", response_class=HTMLResponse)
async def service_detail(request: Request, service_name: str, message: Optional[str] = None):
    compose = Compose()
    try:
        service = compose.get_service(service_name)
        return templates.TemplateResponse(
            "service_detail.html",
            {
                "request": request,
                "title": "Service Detail",
                "service": service,
                "message": message
            }
        )
    except ValueError:
        # If service not found, redirect to home
        return templates.TemplateResponse(
            "home.html",
            {"request": request, "title": "Home", "services": compose.services}
        )

@router.post("/service/{service_name}/env/{envar_name}", response_class=HTMLResponse)
async def update_env_var(
    request: Request,
    service_name: str,
    envar_name: str,
    value: str = Form(...)
):
    compose = Compose()
    try:
        service = compose.get_service(service_name)
        envar = service.get_envar(envar_name)
        envar.value = value
        compose.render()
        return RedirectResponse(
            url=f"/web/service/{service_name}?message=Environment variable {envar_name} updated successfully",
            status_code=303
        )
    except ValueError as e:
        return templates.TemplateResponse(
            "service_detail.html",
            {
                "request": request,
                "title": "Service Detail",
                "service": service,
                "message": f"Error: {str(e)}"
            }
        )
