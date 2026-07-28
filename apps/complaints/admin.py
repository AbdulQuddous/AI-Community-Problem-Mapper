"""Django admin registration for Complaint and its status history."""
from django.contrib import admin

from apps.complaints.models import Complaint, ComplaintStatusHistory


class ComplaintStatusHistoryInline(admin.TabularInline):
    model = ComplaintStatusHistory
    extra = 0
    readonly_fields = ["old_status", "new_status", "changed_by", "updated_at"]  # <-- fixed
    can_delete = False



@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    """
    Admin view for complaints, including a manual "reprocess" action —
    this is the retry mechanism referenced in FR19 for complaints
    whose Gemini enrichment failed.
    """

    list_display = ["id", "category", "status", "priority_score", "user", "created_at"]
    list_filter = ["status", "category", "is_deleted"]
    search_fields = ["description", "user__username"]
    inlines = [ComplaintStatusHistoryInline]
    actions = ["reprocess_enrichment"]

    @admin.action(description="Reprocess AI enrichment for selected complaints")
    def reprocess_enrichment(self, request, queryset):
        """
        FR19's manual retry path: re-triggers enrichment for complaints
        where Gemini calls previously failed (category/priority still
        null). Implemented fully once Phase 6 lands; the signal-based
        mechanism itself is already correct as of this phase.
        """
        import threading

        from apps.ai_engine.services.enrichment_service import enrich_complaint

        count = 0
        for complaint in queryset:
            threading.Thread(
                target=enrich_complaint, args=(str(complaint.id),), daemon=True
            ).start()
            count += 1
        self.message_user(request, f"Reprocessing triggered for {count} complaint(s).")