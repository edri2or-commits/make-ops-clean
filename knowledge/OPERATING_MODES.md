# Operating Modes (Chat) — L2 default

**Purpose**: Define how system operates at different capability levels

---

## Mode Definitions

### L1: Read-Only
**When to use**: 
- Initial system exploration
- Auditing existing state
- User explicitly requests read-only
- Recovery from incidents

**Allowed operations**:
- ✅ GET requests to all APIs
- ✅ List resources
- ✅ Read configurations
- ✅ Collect evidence
- ✅ Generate proof packs

**Prohibited**:
- ❌ Any state changes
- ❌ Write operations
- ❌ DELETE operations
- ❌ Creating resources

**Exit criteria (DoD)**:
- [ ] All APIs verified
- [ ] Evidence Index populated
- [ ] Proof packs created
- [ ] System state documented

---

### L2: Controlled-Write (DEFAULT)
**When to use**:
- Normal operations (default mode)
- Making changes to system
- After L1 DoD completed

**Allowed operations**:
- ✅ All L1 operations
- ✅ Create/Update/Delete resources
- ✅ Push to GitHub (PRs)
- ✅ Modify configurations
- ✅ Run workflows

**Requirements**:
- 📄 PR-first when possible (code changes)
- 🔍 Canary testing before full rollout
- 🔙 Rollback plan documented
- 📊 Immediate proof generation

**Prohibited**:
- ❌ Direct merge to main (require approval)
- ❌ Bulk operations without canary
- ❌ Changes without proof

**Exit criteria (DoD)**:
- [ ] Write operations tested
- [ ] Rollback verified
- [ ] Canary successful
- [ ] Proof packs complete
- [ ] No incidents for 7 days

---

### L3: Automations
**When to use**:
- After L2 DoD completed
- Setting up scheduled tasks
- Implementing triggers
- Full autonomous operation

**Allowed operations**:
- ✅ All L2 operations
- ✅ Schedule workflows
- ✅ Set up triggers
- ✅ Configure monitoring
- ✅ Auto-remediation

**Requirements**:
- 📊 Observability (logs, metrics, alerts)
- 🔔 Notification channels configured
- 🛑 Circuit breakers in place
- 📝 Runbooks for incidents

**Exit criteria (DoD)**:
- [ ] Automations running smoothly
- [ ] Monitoring active
- [ ] Alerts configured
- [ ] Incident response tested
- [ ] No manual intervention for 30 days

---

## Mode Transitions

### L1 → L2
```
1. Complete L1 DoD checklist
2. Review evidence with user
3. Get explicit approval: "Ready for L2"
4. Enable write permissions
5. Document transition in DECISION_LOG.md
```

### L2 → L3
```
1. Complete L2 DoD checklist
2. Verify 7 days incident-free
3. Get explicit approval: "Enable automation"
4. Set up monitoring first
5. Enable automations gradually
6. Document transition in DECISION_LOG.md
```

### Emergency: Any → L1
```
1. Incident detected
2. Immediate pause all writes
3. Revert to read-only
4. Collect incident evidence
5. Fix root cause
6. Restart from L1 DoD
```

---

## Mode Enforcement

### System Flags
```json
{
  "operating_mode": "L2",
  "enforce_layered_flow": true,
  "allow_mode_skip": false,
  "require_approval_for_transition": true
}
```

### Agent Behavior
- **Claude**: Respects mode, enforces DoD
- **GPT**: Respects mode, collects evidence
- **User (Or)**: Can override mode with explicit command

---

## Decision Flow

```
User request → Check current mode → Operation allowed?
                                           │
                                    YES │      │ NO
                                           │      │
                                      Execute    Ask user:
                                           │    "Switch to L2?"
                                           │      │
                                      Generate   YES │   │ NO
                                        Proof        │   │
                                           │    Transition  Stay L1
                                           │      │
                                         Done    Execute
                                                   │
                                              Generate Proof
```

---

**Updated**: 2025-11-12  
**Branch**: unified/desktop-merge  
**Default Mode**: L2 (Controlled-Write)
