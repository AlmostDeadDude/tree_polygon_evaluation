# Tree Polygon Evaluation – demo notes

Tree Polygon Evaluation began as a University of Stuttgart project where contributors on a crowdsourcing platform inspected aerial imagery and rated how accurately pre-drawn polygons followed each tree canopy. Jobs were bundled through the preprocessing scripts, dispatched to workers with the PHP interface, and later aggregated for research using the post-processing utilities.

This folder now hosts a **demo build** that mirrors the front-end experience while keeping the backend read-only. Visitors receive a random archived job, rate every polygon inside the browser, and see the proof code that historically confirmed payment. No new files are written; instead, historic data continues to power the visualisation dashboard.

Key components:

-   `pre_processing*/` – scripts that slice raw datasets into `web/jobs/job_X.txt` files.
-   `web/` – the user interface for onboarding and rating tasks in demo mode.
-   `post_processing/` – aggregation utilities that generate `final_results.txt` for the visualisation.
-   `visualisation/` – the admin dashboard, now exposed publicly to showcase archived outcomes.
