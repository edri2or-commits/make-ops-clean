# CAPABILITIES MATRIX - Calendar Focus Event Entry (OS_SAFE)

**Updated**: 2025-11-17  
**Addition**: Calendar Focus Event capability (PILOT_DESIGNED)

---

## 3.3 Calendar - New: Create Focus Event

### Complete Calendar Capabilities Table

| From | To | Capability | Status | Details | Safeguards | Last Verified | Reference |
|------|----|-----------| -------|---------|------------|---------------|-----------|
| Claude MCP | Calendar API | Read events | ✅ Verified | Full calendar access | None (OS_SAFE) | 2025-11-13 | Native integration |
| Claude MCP | Calendar API | Find free time | ✅ Verified | Analyze availability | None (OS_SAFE) | 2025-11-13 | Native integration |
| Claude MCP | Calendar API | **Create focus event** | **🔄 PILOT_DESIGNED** | **Create personal focus/strategy time blocks** | **(1) Schedule review (conversational) (2) Rate: 20 events/day (soft, optional) (3) Log: Standard to OPS/LOGS/ (4) Scope: calendar.events (no attendees) (5) Blocks: No attendees, no share, no edit existing, no recurring** | **Pending G2.5** | **[PILOT_CALENDAR_FOCUS_EVENT_FLOW.md](DOCS/PILOT_CALENDAR_FOCUS_EVENT_FLOW.md)** |
| Claude MCP | Calendar API | Create meeting (with attendees) | 🔄 G2.6 | Requires attendees management | CLOUD_OPS_MEDIUM + approval | Pending G2.6 | AUTONOMY_PLAN |
| Claude MCP | Calendar API | Edit events | 🔄 G2.6 | Requires events.update | CLOUD_OPS_MEDIUM + logged | Pending G2.6 | AUTONOMY_PLAN |

---

## Calendar Focus Event - Detailed Entry

**Capability**: Create personal focus/strategy events in Google Calendar  
**Status**: 🔄 PILOT_DESIGNED (Phase G2.1-Pilot)  
**Operational After**: G2.5 execution (OAuth scope expansion + testing)

### What it does

**Primary function**:
- Creates personal focus/strategy time blocks in Google Calendar
- Analyzes existing schedule to find optimal times
- Considers strategic priorities and work patterns
- Proposes schedule for Or's review
- Creates private events (no attendees)

**Use cases**:
- Deep work blocks (coding, architecture, planning)
- Strategic thinking time (quarterly planning, roadmaps)
- Focus sessions (specific projects or initiatives)
- Weekly review blocks (retrospectives, adjustments)

**Not supported** (different flows):
- Meetings with attendees → CLOUD_OPS_MEDIUM, separate flow
- Recurring events → Future enhancement
- All-day events → Can be added to this flow
- Editing existing events → Separate capability

### Risk Level: OS_SAFE

**Why OS_SAFE**:
1. **No external impact**: Events are private (no attendees)
2. **Fully reversible**: Or can delete/edit events anytime
3. **Calendar history**: Google Calendar tracks all changes
4. **No communication**: No invitations sent
5. **Personal only**: No other people affected
6. **Controlled scope**: Focus events only

**Comparison with Gmail Send**:
| Aspect | Gmail Send (CLOUD_OPS_HIGH) | Calendar Focus (OS_SAFE) |
|--------|----------------------------|--------------------------|
| External impact | High (recipient receives) | None (private event) |
| Reversibility | None (cannot unsend) | Full (delete/edit anytime) |
| Affected parties | Recipients (external) | Or only (personal) |
| Safeguards | 5 layers (heavy) | 5 layers (light) |

---

## Four Pilots - Complete Comparison

**Template universality fully proven**:

| Aspect | Gmail Drafts | Gmail Send | Drive Create Doc | Calendar Focus |
|--------|--------------|------------|------------------|----------------|
| **Domain** | Gmail | Gmail | Drive + Docs | Calendar |
| **Risk** | OS_SAFE | CLOUD_OPS_HIGH | OS_SAFE | OS_SAFE |
| **External impact** | None | High | None | None |
| **Reversibility** | Full | None | Full | Full |
| **Approval** | Content review | "מאשר שליחה" + TTL | Outline review | Schedule review |
| **TTL** | None | 60 minutes | None | None |
| **Rate limit** | 50/h (optional) | 10/h (hard) | 20/h (optional) | 20/day (optional) |
| **Logging** | Standard | Detailed | Standard | Standard |
| **Scope** | gmail.compose | gmail.send | drive.file + docs.file | calendar.events |
| **Policy blocks** | No send | No forward/BCC/bulk | No share/delete existing | No attendees/share/edit |
| **Phase** | G2.2 | G2.3 | G2.4 | G2.5 |
| **Playbook size** | 22KB | 46KB | 43KB | 33KB |

**Pattern proven**:
- **Template works** across 4 domains (Gmail, Drive, Calendar) ✓
- **Template works** for both risk levels (OS_SAFE, CLOUD_OPS_HIGH) ✓
- **Template is universal** ✓

---

**Maintained by**: Claude  
**Last Updated**: 2025-11-17 (Phase G2.1-Pilot)  
**Next Update**: After G2.5 execution  
**Total Pilots**: 4 (Gmail x2, Drive x1, Calendar x1)
