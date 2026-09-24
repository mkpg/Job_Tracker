# Job Interview Reminder Automation — n8n

An n8n automation connected to PostgreSQL/Neon and Gmail that checks job applications and sends a reminder when an expected interview/application date is approaching.

## Workflow

```text
Schedule Trigger
       |
       v
PostgreSQL
       |
       v
IF: expected date is near + reminder_sent = false
       |
       v
Gmail
       |
       v
PostgreSQL
       |
       v
reminder_sent = true
```

## What it does

1. Runs automatically once per day.
2. Reads job applications from PostgreSQL/Neon.
3. Checks whether an expected date is within the reminder window.
4. Sends a Gmail reminder to the user's email.
5. Updates `reminder_sent` to `true`.
6. Prevents the same application from receiving the reminder repeatedly.

## Example email

**Subject:** Interview Reminder

```text
Hi,

Prepare well, you are near.

Company: [Company]
Position: [Job Name]
Expected Date: [Expected Date]
```

## Database fields used

```text
job_id
user_id
job_name
company
status
apply_date
expected_date
reminder_sent
email
```

The `email` value can come from a joined query or another user table, depending on the application database design.

## n8n nodes

- Schedule Trigger
- PostgreSQL — Execute a SQL query
- IF
- Gmail — Send a message
- PostgreSQL — Execute a SQL query

## Security

The real n8n workflow and credentials are kept locally.

This repository contains only:

- a workflow screenshot
- a sanitized example JSON
- documentation

No real:

- Neon/PostgreSQL password
- Gmail OAuth secret
- OAuth access/refresh token
- API key
- database connection string
- personal email address

The file `workflow/workflow-example.json` is **not the real exported n8n workflow**. It is a safe documentation example showing the workflow structure and sample configuration.

## Setup concept

Create your own credentials inside your local n8n instance:

```text
PostgreSQL credential
        +
Gmail OAuth credential
        ↓
Configure the nodes
        ↓
Activate the workflow
```

## Project Context

This automation is part of a Job Application Tracker built with Flask, PostgreSQL/Neon, and n8n.

The application stores job information in PostgreSQL, while n8n handles the scheduled reminder automation.

## Screenshot

See `screenshots/workflow.png` for the workflow layout.
