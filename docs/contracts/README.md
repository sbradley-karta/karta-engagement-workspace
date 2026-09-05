# Contracts, version 1

Three documents define how the engagement site, the assembly service, and the engagement record talk to each other. They are designed once and shared by the target path (Cloud Run service) and the documented fallback (cloud routine). Nothing in the review or approval surface depends on which assembler runs.

| Contract | Written by | Read by | Schema |
|---|---|---|---|
| Approved values | The engagement site, at Approve | The assembly service; the engagement record | `approved-values.v1.schema.json` |
| Deck job | The engagement site, at Generate deck; updated by whichever assembler runs | The engagement site | `deck-job.v1.schema.json` |
| Engagement configuration | Engagement setup, reviewed by the engagement lead | The engagement site | `engagement-config.v1.schema.json` |

## Rules the schemas enforce

1. **Derived fields are derived in code.** Milestone status, date variance, the status period, and the overall rollup are computed by `karta_assembler.status` and stamped into approved values. The model never sets them. The service recomputes and refuses a document whose derived fields disagree with its inputs.
2. **New Date governs.** When a milestone carries both an original and an approved new date, status is judged against the new date. The original date is kept for the variance column only.
3. **Missing evidence is never Green.** A milestone with no governing date is `Unknown`. An assessment the reviewer has not judged is `Not assessed`. The overall rollup cannot be `Green` while any assessment is `Unknown` or `Not assessed`.
4. **Named approval is part of the document.** Approved values carry the reviewer's name, email, timestamp, and version. A document without them is a draft and the service refuses it.
5. **Size bound.** Serialized approved values must stay under 524,288 bytes. Gate 1 measured the page-to-connector request ceiling at about 1 MiB; this leaves headroom for the envelope.
6. **Provenance travels with the record.** Every milestone and RAID item names its source system and identifier. Sources list retrieval time so freshness can be shown.
7. **Correction capture.** Approved values record which fields the model drafted and which the reviewer changed, so the correction rate can be measured without storing prompts.

## Amendments

- **1.0, September 5, 2026.** RAID items gained optional `priority` (High, Medium, Low) and `mitigation`, because the status slide's risks table shows a priority tag and a Mitigation Plan column. Backward compatible.

## Slide 4 shape map (from the sample deck, matches the existing skill)

| Shape | Content |
|---|---|
| `Table 8` | Row 1 Project Name, row 2 Project Manager(s), row 3 Status Period |
| `Table 9` | Row 1 Overall Status text, rows 2 to 4 Scope & Schedule, Resources, Data |
| `Oval 22`, `Oval 1`, `Oval 11`, `Oval 12` | Status colors for Overall, Scope & Schedule, Resources, Data. Theme colors: Green is accent1, Yellow is accent5, Red is accent6, Unknown is the neutral background 2 |
| `Table 14` | Milestones: Milestone, Orig. Date, New Date, Status. One header row plus ten data rows |
| `Table 16` | Row 2: Accomplishments (column 1), Planned Activities (column 2), bulleted |
| `Table 19` | Risks or Issue, Description, Mitigation Plan, Status. One header row plus three data rows |
| Slide 1 `Text Placeholder 2` | Deck date |

## Milestone status rule (confirmed by Sean, September 5, 2026)

| Condition, evaluated in order | Status |
|---|---|
| Task completed | Complete |
| No original date and no new date | Unknown |
| Governing date (new date if present, else original) is before the as-of date | Off Track |
| New date present and later than the original date | At Risk |
| Otherwise | On Track |

Variance in days is `new_date - original_date`, or null when either is missing.

## Overall rollup rule

Worst of Scope and Schedule, Resources, and Data: any Red gives Red; else any Yellow gives Yellow; else any Unknown or Not assessed gives Unknown; else Green.

## Status period

The Monday through Friday work week containing the as-of date.
