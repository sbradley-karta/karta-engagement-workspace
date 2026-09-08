# Cross-engagement access tests

**Purpose:** prove that a member sees only the engagements they are staffed on, across retrieval, storage, logs, and generated files. Run at stand-up of every engagement and whenever the manifest or the service changes. Record results in the handover.

**People:** A, a member staffed on the engagement under test. B, a Karta member with a Claude seat who is not staffed on it in Asana or SharePoint. Sean as observer.

| # | Area | Test | Expected | Result |
|---|---|---|---|---|
| 1 | Retrieval, Asana | B opens the engagement page | Asana chip is red or shows zero tasks; Milestones view is empty; Home shows no milestones | |
| 2 | Retrieval, SharePoint | B opens Weekly status, Review sources | No status deck found; source gap recorded | |
| 3 | Retrieval, Ask Claude | B asks "What are the milestones?" | Answer states the evidence is missing; cites no task names | |
| 4 | Storage, approved record | B opens Decisions and Artifacts | Approved records are visible only if B was shared the page; confirm B was not shared, and the page cannot be opened at all | |
| 5 | Storage, second engagement | A opens the other engagement's page | A sees nothing from sources they are not staffed on; approved records visible only if shared | |
| 6 | Logs | Sean reads Cloud Run logs for the assembly service | Request metadata only; no approved values, names, or deck content in logs | |
| 7 | Generated files, interim | A generates a deck | Deck contains only this engagement's approved values; file saved by A only | |
| 8 | Generated files, target mode | A generates a deck after sign-in is restored | Deck lands in this engagement's folder as A; B cannot open the folder | |
| 9 | Connector scope | B lists connectors | Karta Assembly is visible (org connector) but returns nothing useful without approved values from a page B can open | |
| 10 | Sharing | Sean reviews the page's share list | Staffed members only; no public link | |

Pass criterion: every row passes. Any failure blocks client-facing use until fixed and re-tested.

Known limits this plan accepts for the pilot: approved records and deck jobs live in the page's database, which every viewer who can open the page can read. Isolation of records therefore rests on page sharing, which is why row 10 exists. Server-enforced record boundaries are a Horizon 2 item.
