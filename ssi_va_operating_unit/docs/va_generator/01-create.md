# Create Virtual Account Generator

> **Module:** ssi_va_operating_unit
> **Extends:** ssi_va — model `va_generator`, aksi `01-create`

## Additional Fields

When this module is installed, the following field is available on both the **Generate
VA** wizard and the `va_generator` document form:

- **Operating Unit**: The operating unit the generated Virtual Account Generator
  document belongs to. Not required. Automatically filled from the user's default
  operating unit. Change if needed. Only visible to users in the
  `operating_unit.group_multi_operating_unit` group.

## Additional Pre-Condition

- **Module:** `ssi_va_operating_unit` is installed.
- **Access:** User is in the `operating_unit.group_multi_operating_unit` group, so the
  **Operating Unit** field is visible.

## Modified — Record Visibility

- The **VA Generators** list is now filtered by operating unit (record rule). A user
  only sees `va_generator` documents whose **Operating Unit** is one of the operating
  units assigned to them. This is not a Flow step.
