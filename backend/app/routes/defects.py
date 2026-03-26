from flask.views import MethodView
from flask_smorest import Blueprint, abort

from app.defects_store import STORE
from app.schemas.defects import DefectCreateSchema, DefectSchema, DefectUpdateSchema

blp = Blueprint(
    "Defects",
    "defects",
    url_prefix="/defects",
    description="CRUD endpoints for quality defects (demo-safe, in-memory).",
)


@blp.route("")
class DefectsCollection(MethodView):
    def get(self):
        """
        List defects.

        Returns an array of all defects in memory.
        """
        return STORE.list()

    @blp.arguments(DefectCreateSchema)
    @blp.response(201, DefectSchema)
    def post(self, payload):
        """
        Create a new defect.

        Accepts a defect payload and returns the created defect.
        """
        created = STORE.create(payload)
        return created


@blp.route("/<string:defect_id>")
class DefectItem(MethodView):
    @blp.response(200, DefectSchema)
    def get(self, defect_id: str):
        """
        Get defect by id.
        """
        defect = STORE.get(defect_id)
        if not defect:
            abort(404, message="Defect not found")
        return defect

    @blp.arguments(DefectUpdateSchema)
    @blp.response(200, DefectSchema)
    def put(self, payload, defect_id: str):
        """
        Update defect by id (patch semantics).

        Only provided fields are updated.
        """
        updated = STORE.update(defect_id, payload)
        if not updated:
            abort(404, message="Defect not found")
        return updated

    def delete(self, defect_id: str):
        """
        Delete defect by id.

        Returns 204 on success.
        """
        ok = STORE.delete(defect_id)
        if not ok:
            abort(404, message="Defect not found")
        return ("", 204)
