# Add Generate VA Wizard

> **Module:** ssi_va\
> **Model:** `ir.model`\
> **Menu:** Settings > Technical > Database Structure > Models\
> **Actor:** user in group `base.group_system` (Settings)\
> **Extends:** base — model `ir.model`

## Pre-Condition

- **Access:** User is in group `base.group_system` (Settings), matching the
  `groups="base.group_system"` attribute on the **Add Generate VA Wizard** button.
- **Record:** The selected model is not a transient model (its **Transient Model**
  checkbox is unchecked). Transient models are rejected — their records do not survive
  past the transaction, so they can never be a valid Virtual Account source.

## Flow

1. Open the **Settings > Technical > Database Structure > Models** menu. (Developer mode
   must be enabled to see the **Technical** menu.)
2. Open the record of the model that should become a Virtual Account source.
3. Click the **Add Generate VA Wizard** button (`action_create_va_wizard`) in the
   header.
   - If the model is a transient model, the action fails with a `UserError` explaining
     that the model cannot be a valid Virtual Account source, and no binding is created.
     Select a non-transient model instead.
4. Optional: click **Add Generate VA Wizard** again on the same record. Pressing it
   repeatedly is allowed — each press creates a new, separately named binding instead of
   being rejected as a duplicate. The first press names the binding **Generate VA**;
   each following press is numbered (**Generate VA #2**, **Generate VA #3**, …).

## Post-Condition

- A new entry appears in the model's **Action** menu, visible from both the list view
  and the form view of that model — named **Generate VA** (or **Generate VA #N** for
  subsequent presses).
- From that **Action** menu entry, the **Generate VA** wizard can now be run against
  records of the selected model.
