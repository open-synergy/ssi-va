# Edit Virtual Account Generator

> **Module:** ssi_va_operating_unit
> **Extends:** ssi_va — model `va_generator`, aksi `02-edit`

## Additional Fields

When this module is installed, the `va_generator` document form gains the following
field, which can still be changed while editing (it does not carry a per-state readonly
restriction):

- **Operating Unit**: The operating unit the document belongs to. Not required. Only
  visible to users in the `operating_unit.group_multi_operating_unit` group.

## Additional Pre-Condition

- **Module:** `ssi_va_operating_unit` is installed.
- **Access:** User is in the `operating_unit.group_multi_operating_unit` group, so the
  **Operating Unit** field is visible.
