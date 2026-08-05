# Create Virtual Account Generator Type

> **Module:** ssi_va\
> **Model:** `va_generator_type`\
> **Menu:** Financial Accounting > Configuration > Virtual Account > Generator Types\
> **Actor:** user in group `Virtual Account Generator Type`\
> **Inline Actions:** `action_generate_code` (Generate Code)

## Pre-Condition

- **Config:** An active `sequence.template` for model `va_generator_type` is configured.
  Only needed if the **Generate Code** button will be used to auto-assign the **Code**
  field.
- **Access:** User is in group `Virtual Account Generator Type`.

## Flow

1. Open the **Financial Accounting > Configuration > Virtual Account > Generator Types**
   menu.
2. Click the **Create** button.
3. Fill in the required fields:
   - **Name** _(required)_: Enter a name that identifies this generator type.
   - **Code** _(required)_: Enter a unique code, or enter **/** to leave it blank for
     now and assign it later with the **Generate Code** button.
4. Optionally, fill in the **Restrict to Model** field. When set, this generator type
   can only be selected from the VA generation wizard when run from the selected model.
   Left empty, it is available for all models.
5. Click **Generate Code** in the header to assign a value to the **Code** field from
   the configured sequence template. Only applies when **Code** is still **/** — records
   with a manually entered code are left unchanged. Skip this step if a code was already
   entered manually in step 3.
6. On the **Python Code** tab, review/edit the **Python Code** field _(required)_. This
   code is executed (via `safe_eval`) to compute the unique Virtual Account code and
   **must assign a string to the variable `result`**. In addition to the standard
   safe_eval helpers (`env`, `document`, `time`, `datetime`, `dateutil`, `timezone`,
   `float_compare`, `b64encode`, `b64decode`), the following variables are available:
   `biller`, `merchant`, `bank`, `partner`, `source_data`, `source_record`. A default
   value (`result = ""`) is pre-filled; replace it with the actual computation logic.
7. On the **Partner Resolution Python Code** tab, review/edit the **Partner Resolution
   Python Code** field _(required)_. This code is executed (via `safe_eval`) to resolve
   the current source data line into the `res.partner` record Virtual Account numbers
   are generated for, and **must assign exactly one `res.partner` record to the variable
   `result`**. In addition to the standard safe_eval helpers listed above, the following
   variables are available: `generator`, `source_data`, `source_record`, `biller`,
   `merchant`. A default value (`result = source_data.source_data_id`) is pre-filled;
   replace it with the actual resolution logic.
8. Click **Save**.

## Post-Condition

- A new **Virtual Account Generator Type** record is created and appears in the
  Generator Types list.
- If **Generate Code** was used, the **Code** field now holds a value from the
  configured sequence template.
