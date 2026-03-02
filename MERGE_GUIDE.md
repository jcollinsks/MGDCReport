# Merge Guide: Adding Security Analysis to Your Lakehouse-Connected Report

This guide explains how to add the MGDC security analysis (calculated columns, 120 DAX measures, relationships, and 10 report pages) into a blank Power BI report that already has a working connection to your Fabric Lakehouse.

## Prerequisites

- Power BI Desktop with your blank report saved as a `.pbip` project
- The 5 MGDC tables already connected and loading from your Lakehouse:
  - `SharePoint_Sites_v1`
  - `SharePoint_Files_v1`
  - `SharePoint_FileActions_v1`
  - `SharePoint_Permissions_v1`
  - `SharePoint_Groups_v1`

## Your Project Structure

After saving as PBIP, your project should look like this:

```
YourProject.pbip
YourProject.SemanticModel/
  definition.pbism
  .platform
  definition/
    database.tmdl
    model.tmdl
    expressions.tmdl              <-- Lakehouse connection (keep as-is)
    tables/
      SharePointSites.tmdl        <-- has working partition (keep as-is)
      SharePointFiles.tmdl
      SharePointFileActions.tmdl
      SharePointPermissions.tmdl
      SharePointGroups.tmdl
YourProject.Report/
  definition.pbir
  .platform
  definition/
    report.json
    version.json
    pages/
```

## Step 1: Add Calculated Columns to Each Table

Open each table TMDL file in a text editor. You will see the source columns and a `partition` block at the bottom. Paste the calculated columns **before** the `partition` line.

Copy the calculated columns from the corresponding files in this repo under `MGDCSecurityDashboard.SemanticModel/definition/tables/`.

### SharePointSites.tmdl — 11 calculated columns

Paste these before the `partition` line. Copy from the repo file starting at `column CalcSiteRiskScore =` through the last `annotation SummarizationSetBy = Automatic` for `IsOverprovisioned`.

| Column | Type | Description |
|--------|------|-------------|
| `CalcSiteRiskScore` | int64 | Composite risk score 0-100 (sharing +25, no label +20, no device policy +15, orphaned +15, stale +15, no CA +10) |
| `SiteRiskTier` | string | Critical (>=75), High (>=50), Medium (>=25), Low |
| `SiteType` | string | Communication, Personal, or Team |
| `StorageUsedGB` | double | Storage in GB |
| `DaysSinceModified` | int64 | Days since last modification |
| `ExternalSharingRiskLevel` | string | Critical/High/Medium/Low based on SharingCapability |
| `IsOrphaned` | boolean | True if no OwnerEmail |
| `HasSensitivityLabel` | boolean | True if SensitivityLabelId is not blank |
| `StorageUtilizationPct` | double | Percentage of allocated storage used |
| `SiteAgeCategory` | string | New (<90d), Recent (<1yr), Established (<2yr), Mature |
| `IsOverprovisioned` | boolean | True if <5% utilization and >1GB allocated |

### SharePointFiles.tmdl — 10 calculated columns

Copy from the repo file starting at `column FileSizeMB =`.

| Column | Type | Description |
|--------|------|-------------|
| `FileSizeMB` | double | File size in MB |
| `FileCategory` | string | Documents, Spreadsheets, Presentations, PDFs, Images, Other |
| `SecurityStatus` | string | Protected, Encrypted Only, Labeled Only, Unprotected |
| `HasSensitivityLabel` | boolean | True if labeled |
| `FileAgeCategory` | string | New/Recent/Standard/Old/Ancient |
| `IsLargeFile` | boolean | True if >100MB |
| `VersionBloatRatio` | double | Version storage / file size |
| `DaysSinceModified` | int64 | Days since last modification |
| `IsStale` | boolean | True if >180 days since modified |
| `FileRiskScore` | int64 | Composite file risk 0-100 |

### SharePointFileActions.tmdl — 10 calculated columns

Copy from the repo file starting at `column ActionDate =`.

| Column | Type | Description |
|--------|------|-------------|
| `ActionDate` | dateTime | Date-only key for DimDate relationship |
| `ActionHour` | int64 | Hour of day (0-23) |
| `IsWeekend` | boolean | Saturday or Sunday |
| `IsAfterHours` | boolean | Before 7am or after 7pm |
| `IsHighRiskAction` | boolean | Delete, Manage, or Share actions |
| `IsSuspiciousActivity` | boolean | After-hours AND high-risk AND external |
| `ActionCategory` | string | Read, Write, Delete, Manage |
| `UserAgentCategory` | string | Teams, OneDrive, Browser, Mobile, API, Other |
| `IsExternalDownload` | boolean | External user + download action |
| `TimePeriod` | string | Morning, Afternoon, Evening, Night |

### SharePointPermissions.tmdl — 11 calculated columns

Copy from the repo file starting at `column IsAnonymousLink =`.

**Important:** `IsAnonymousLink`, `IsExternalShare`, and `HasNoExpiration` must come before `PermissionRiskLevel` since it depends on them.

| Column | Type | Description |
|--------|------|-------------|
| `IsAnonymousLink` | boolean | Anonymous sharing link |
| `IsExternalShare` | boolean | External user share |
| `HasNoExpiration` | boolean | Link never expires |
| `PermissionRiskLevel` | string | Critical/High/Medium/Low |
| `PermissionRiskScore` | int64 | 100/75/50/25 by risk level |
| `IsOverprivileged` | boolean | Full Control or Owner role |
| `PermissionAgeCategory` | string | New/Recent/Standard/Old/Ancient |
| `PermissionAgeDays` | int64 | Days since permission created |
| `DaysUntilExpiry` | int64 | Days until link expires |
| `IsExpiringSoon` | boolean | Expires within 30 days |
| `LinkCategory` | string | Direct (if no link type) or LinkType value |

### SharePointGroups.tmdl — 5 calculated columns

Copy from the repo file starting at `column IsOwnerless =`.

**Important:** `IsOwnerless`, `IsOverlarge`, and `ExternalMemberPct` must come before `GroupRiskLevel` since it depends on them.

| Column | Type | Description |
|--------|------|-------------|
| `IsOwnerless` | boolean | Zero owners |
| `IsOverlarge` | boolean | >100 members |
| `ExternalMemberPct` | double | Percentage of external members |
| `GroupRiskLevel` | string | Critical/High/Medium/Low |
| `GroupSizeCategory` | string | Small/Medium/Large/Very Large |

### What a calculated column looks like in TMDL

Each calculated column block follows this pattern (note the tab indentation):

```
	column CalcSiteRiskScore =
		VAR _ExternalSharing = IF([SharingCapability] IN {"ExternalUserAndGuestSharing", "ExternalUserSharingOnly"}, 25, 0)
		VAR _NoLabel = IF(ISBLANK([SensitivityLabelId]), 20, 0)
		RETURN _ExternalSharing + _NoLabel
		dataType: int64
		lineageTag: c1a00001-0001-0001-0001-000000000201
		summarizeBy: none

		annotation SummarizationSetBy = Automatic
```

Key rules:
- Lines use **tabs** for indentation, not spaces
- The `= DAX expression` goes on the same line as `column Name` (or continues on indented lines below)
- Properties (`dataType`, `lineageTag`, `summarizeBy`) are indented with **two tabs**
- The `annotation` is indented with **two tabs**
- Blank line between each column block

---

## Step 2: Copy New Table Files

Copy these two files from this repo's `MGDCSecurityDashboard.SemanticModel/definition/tables/` folder into your project's `tables/` folder:

### `_Measures.tmdl`

Contains 120 DAX measures organized in 10 display folders:

| # | Display Folder | Count | Examples |
|---|---------------|-------|---------|
| 1 | Executive Overview | 12 | Total Sites, Security Score, Security Grade |
| 2 | External Sharing | 14 | Anonymous Links, Never Expiring Links |
| 3 | Permission Analysis | 14 | Critical Risk Permissions, Sprawl Index |
| 4 | Sensitivity & Encryption | 12 | File Label Coverage Pct, Unprotected Pct |
| 5 | User Activity | 16 | After Hours Pct, Suspicious Activities |
| 6 | Site Security | 10 | Orphaned Sites, Sites Missing Conditional Access |
| 7 | Group Risks | 11 | Ownerless Groups, External Members |
| 8 | File Intelligence | 11 | Reclaimable Storage GB, Avg Version Bloat Ratio |
| 9 | Stale Access | 10 | Stale Files, Zombie Links |
| 10 | Risk Scoring | 10 | Composite Risk Index, Data Exposure Score |

### `DimDate.tmdl`

Calculated date dimension table (2020-2026) with columns: Date, Year, MonthNumber, MonthName, Quarter, DayOfWeek, DayName, IsWeekend, YearMonth, YearQuarter.

Used for time-based relationships with FileActions and Permissions.

---

## Step 3: Update model.tmdl

Open your `model.tmdl` file. It will look something like:

```
model Model
	culture: en-US
	defaultPowerBIDataSourceVersion: powerBI_V3
	sourceQueryCulture: en-US

annotation PBI_QueryOrder = [...]

ref table SharePointSites
ref table SharePointFiles
...
```

### 3a. Add ref table lines

Add these two lines alongside the existing `ref table` entries (at root level, no indentation):

```
ref table DimDate
ref table _Measures
```

### 3b. Add relationships

Add all of the following at the bottom of the file (at root level, no indentation). Relationship properties are indented with one tab.

```
relationship 9c3a7b1e-4d2f-4a8e-b6c1-d5e7f9a0b2c4
	fromColumn: SharePointFiles.SiteId
	toColumn: SharePointSites.SiteId

relationship a4b8c2d6-5e3f-4b9a-c7d1-e6f0a1b3c5d7
	fromColumn: SharePointFileActions.SiteId
	toColumn: SharePointSites.SiteId

relationship b5c9d3e7-6f4a-4c0b-d8e2-f7a1b2c4d6e8
	fromColumn: SharePointPermissions.SiteId
	toColumn: SharePointSites.SiteId

relationship c6d0e4f8-7a5b-4d1c-e9f3-a8b2c3d5e7f9
	fromColumn: SharePointGroups.SiteId
	toColumn: SharePointSites.SiteId

relationship d7e1f5a9-8b6c-4e2d-f0a4-b9c3d4e6f8a0
	isActive: false
	fromColumn: SharePointFileActions.FileId
	toColumn: SharePointFiles.FileId

relationship e8f2a6b0-9c7d-4f3e-a1b5-c0d4e5f7a9b1
	isActive: false
	fromColumn: SharePointPermissions.FileId
	toColumn: SharePointFiles.FileId

relationship f9a3b7c1-0d8e-4a4f-b2c6-d1e5f6a8b0c2
	fromColumn: SharePointFileActions.ActionDate
	toColumn: DimDate.Date

relationship a0b4c8d2-1e9f-4b5a-c3d7-e2f6a7b9c1d3
	isActive: false
	fromColumn: SharePointPermissions.CreatedDateTime
	toColumn: DimDate.Date
```

### Relationship summary

| From | To | Active | Purpose |
|------|-----|--------|---------|
| Files.SiteId | Sites.SiteId | Yes | Files belong to sites |
| FileActions.SiteId | Sites.SiteId | Yes | Actions happen on sites |
| Permissions.SiteId | Sites.SiteId | Yes | Permissions belong to sites |
| Groups.SiteId | Sites.SiteId | Yes | Groups belong to sites |
| FileActions.FileId | Files.FileId | **No** | Inactive to avoid ambiguous path (use USERELATIONSHIP in DAX) |
| Permissions.FileId | Files.FileId | **No** | Inactive to avoid ambiguous path |
| FileActions.ActionDate | DimDate.Date | Yes | Time intelligence for actions |
| Permissions.CreatedDateTime | DimDate.Date | **No** | Secondary date relationship |

The FileId relationships are inactive because they would create two paths from FileActions/Permissions to Sites (direct via SiteId, and indirect via Files.SiteId). Power BI does not allow ambiguous paths.

---

## Step 4: Copy Report Pages

### 4a. Copy report definition files

From this repo's `MGDCSecurityDashboard.Report/definition/`, copy into your project's `Report/definition/` folder (overwriting the defaults):

- `report.json` — theme and report settings
- `version.json` — version metadata

### 4b. Copy all pages

Copy the entire `pages/` folder from this repo's `MGDCSecurityDashboard.Report/definition/pages/` into your project's `Report/definition/pages/`, replacing what PBI Desktop generated.

This includes:

| Folder | Page Title | Visuals |
|--------|-----------|---------|
| `executive_overview/` | Executive Security Overview | 10 (6 cards + gauge + bar + line + table) |
| `external_sharing/` | External Sharing Exposure | 10 (6 cards + 2 donuts + bar + table) |
| `permission_analysis/` | Permission Deep Dive | 8 (4 cards + 2 donuts + column + table) |
| `sensitivity_encryption/` | Sensitivity & Encryption | 8 (4 cards + donut + 2 bars + table) |
| `user_activity/` | User Activity & Anomalies | 11 (7 cards + line + 2 bars + table) |
| `site_security/` | Site Security Posture | 8 (4 cards + donut + 2 bars + table) |
| `group_risks/` | Group & Membership Risks | 8 (4 cards + donut + 2 bars + table) |
| `file_intelligence/` | File Intelligence & Storage | 8 (4 cards + donut + 2 bars + table) |
| `stale_access/` | Stale Content & Zombie Permissions | 8 (4 cards + 2 donuts + bar + table) |
| `risk_scoring/` | Risk Scoring & Recommendations | 8 (4 cards + donut + bar + column + table) |

Each folder contains a `page.json` and a `visuals/` subfolder with individual visual JSON files.

**Total: 87 visuals across 10 pages.**

Also copy `pages.json` which controls the page ordering.

---

## Step 5: Save and Reopen

1. Close Power BI Desktop
2. Reopen your `.pbip` file
3. You should see:
   - 7 tables in the model (5 Lakehouse + DimDate + _Measures)
   - 120 measures organized in display folders
   - 8 relationships in the model diagram
   - 10 report pages with visuals
4. Click **Refresh** to load data from your Lakehouse
5. Visuals should populate with your data

## Troubleshooting

### "Unexpected line type Empty" error
A `///` comment is followed by a blank line. Remove the comment or the blank line.

### "Ambiguous paths" error
Make sure the FileId relationships for FileActions and Permissions have `isActive: false`.

### Calculated column errors
Make sure dependency columns are defined before the columns that reference them. For example, `IsAnonymousLink` must come before `PermissionRiskLevel` in the Permissions table.

### Visuals show errors
Verify the table and column names in your Lakehouse match what the visuals expect. The visuals reference columns like `SharePointSites[CalcSiteRiskScore]` and measures like `_Measures[Total Sites]`.

### TMDL indentation issues
TMDL requires **tabs** not spaces. If you copy-paste, make sure your editor preserves tabs. Use `cat -A filename.tmdl` on Mac/Linux to verify (`^I` = tab).
