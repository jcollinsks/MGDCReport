#!/usr/bin/env python3
"""
Patch PBI Desktop-generated TMDL files with calculated columns, measures, and relationships.

Usage:
    1. Open Power BI Desktop and connect to Azure SQL (mgdc-test-srv.database.windows.net / MGDCTest)
    2. Add all 5 tables: SPOSites, SPOFiles, SPOFileActions, SPOPermissions, SPOGroups
    3. Save the .pbip file
    4. Close Power BI Desktop completely
    5. Run: python patch_model.py
    6. Reopen the .pbip in Power BI Desktop

This script injects:
- 44 calculated columns across all 5 tables
- 95 DAX measures in a _Measures table
- 6 relationships in model.tmdl
"""

import os
import re
import sys

# Auto-detect the SemanticModel definition directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Try common locations
CANDIDATES = [
    os.path.join(SCRIPT_DIR, 'MGDCSecurityDashboard.SemanticModel', 'definition'),
    # If run from inside the SemanticModel folder
    os.path.join(SCRIPT_DIR, 'definition'),
]

BASE = None
for c in CANDIDATES:
    if os.path.isdir(c):
        BASE = c
        break

if BASE is None:
    # Search for any .SemanticModel/definition directory
    for entry in os.listdir(SCRIPT_DIR):
        candidate = os.path.join(SCRIPT_DIR, entry, 'definition')
        if entry.endswith('.SemanticModel') and os.path.isdir(candidate):
            BASE = candidate
            break

if BASE is None:
    print("ERROR: Could not find SemanticModel/definition directory.")
    print("Run this script from the repo root containing the .SemanticModel folder.")
    sys.exit(1)

TABLES = os.path.join(BASE, 'tables')

# ============================================================
# Calculated columns for each table
# ============================================================

CALC_COLS = {
    'SPOSites': '''\
\tcolumn CalcSiteRiskScore =
\t\t\tVAR _ExternalSharing = IF([IsExternalSharingEnabled], 25, 0)
\t\t\tVAR _NoLabel = IF(ISBLANK([SensitivityLabelInfo.Id]), 20, 0)
\t\t\tVAR _NoDevicePolicy = IF(NOT([BlockAccessFromUnmanagedDevices]), 15, 0)
\t\t\tVAR _Orphaned = IF(ISBLANK([Owner.Email]), 15, 0)
\t\t\tVAR _Stale = IF(DATEDIFF([LastContentChange], TODAY(), DAY) > 180, 15, 0)
\t\t\tVAR _ReadLocked = IF([ReadLocked], 10, 0)
\t\t\tRETURN _ExternalSharing + _NoLabel + _NoDevicePolicy + _Orphaned + _Stale + _ReadLocked
\t\tdataType: int64
\t\tlineageTag: c1a00001-0001-0001-0001-000000000201
\t\tsummarizeBy: none

\t\tannotation SummarizationSetBy = Automatic

\tcolumn SiteRiskTier = SWITCH(TRUE(), [CalcSiteRiskScore] >= 75, "Critical", [CalcSiteRiskScore] >= 50, "High", [CalcSiteRiskScore] >= 25, "Medium", "Low")
\t\tdataType: string
\t\tlineageTag: c1a00001-0001-0001-0001-000000000202
\t\tsummarizeBy: none

\t\tannotation SummarizationSetBy = Automatic

\tcolumn SiteType = SWITCH(TRUE(), [IsOneDrive], "Personal", [IsCommunicationSite], "Communication", "Team")
\t\tdataType: string
\t\tlineageTag: c1a00001-0001-0001-0001-000000000203
\t\tsummarizeBy: none

\t\tannotation SummarizationSetBy = Automatic

\tcolumn StorageUsedGB = DIVIDE([StorageUsed], 1073741824, 0)
\t\tdataType: double
\t\tlineageTag: c1a00001-0001-0001-0001-000000000204
\t\tsummarizeBy: none
\t\tformatString: #,0.00

\t\tannotation SummarizationSetBy = Automatic

\tcolumn DaysSinceModified = DATEDIFF([LastContentChange], TODAY(), DAY)
\t\tdataType: int64
\t\tlineageTag: c1a00001-0001-0001-0001-000000000205
\t\tsummarizeBy: none

\t\tannotation SummarizationSetBy = Automatic

\tcolumn ExternalSharingRiskLevel = IF([IsExternalSharingEnabled], "High", "Low")
\t\tdataType: string
\t\tlineageTag: c1a00001-0001-0001-0001-000000000206
\t\tsummarizeBy: none

\t\tannotation SummarizationSetBy = Automatic

\tcolumn IsOrphaned = ISBLANK([Owner.Email])
\t\tdataType: boolean
\t\tlineageTag: c1a00001-0001-0001-0001-000000000207
\t\tsummarizeBy: none
\t\tformatString: """TRUE"";""TRUE"";""FALSE"""

\t\tannotation SummarizationSetBy = Automatic

\tcolumn HasSensitivityLabel = NOT(ISBLANK([SensitivityLabelInfo.Id]))
\t\tdataType: boolean
\t\tlineageTag: c1a00001-0001-0001-0001-000000000208
\t\tsummarizeBy: none
\t\tformatString: """TRUE"";""TRUE"";""FALSE"""

\t\tannotation SummarizationSetBy = Automatic

\tcolumn StorageUtilizationPct = DIVIDE([StorageUsed], [StorageQuota], 0) * 100
\t\tdataType: double
\t\tlineageTag: c1a00001-0001-0001-0001-000000000209
\t\tsummarizeBy: none
\t\tformatString: #,0.00

\t\tannotation SummarizationSetBy = Automatic

\tcolumn SiteAgeCategory = SWITCH(TRUE(), DATEDIFF([CreatedTime], TODAY(), DAY) < 90, "New", DATEDIFF([CreatedTime], TODAY(), DAY) < 365, "Recent", DATEDIFF([CreatedTime], TODAY(), DAY) < 730, "Established", "Mature")
\t\tdataType: string
\t\tlineageTag: c1a00001-0001-0001-0001-000000000210
\t\tsummarizeBy: none

\t\tannotation SummarizationSetBy = Automatic

\tcolumn IsOverprovisioned = [StorageUtilizationPct] < 5 && [StorageQuota] > 1073741824
\t\tdataType: boolean
\t\tlineageTag: c1a00001-0001-0001-0001-000000000211
\t\tsummarizeBy: none
\t\tformatString: """TRUE"";""TRUE"";""FALSE"""

\t\tannotation SummarizationSetBy = Automatic
''',
    'SPOFiles': '''\
\tcolumn FileSizeMB = DIVIDE([SizeInBytes], 1048576, 0)
\t\tdataType: double
\t\tlineageTag: c1a00002-0001-0001-0001-000000000201
\t\tsummarizeBy: none
\t\tformatString: #,0.00

\t\tannotation SummarizationSetBy = Automatic

\tcolumn FileCategory = SWITCH(TRUE(), [Extension] IN {".docx", ".doc", ".odt", ".rtf"}, "Documents", [Extension] IN {".xlsx", ".xls", ".csv"}, "Spreadsheets", [Extension] IN {".pptx", ".ppt"}, "Presentations", [Extension] IN {".pdf"}, "PDFs", [Extension] IN {".jpg", ".png", ".gif", ".bmp", ".svg"}, "Images", "Other")
\t\tdataType: string
\t\tlineageTag: c1a00002-0001-0001-0001-000000000202
\t\tsummarizeBy: none

\t\tannotation SummarizationSetBy = Automatic

\tcolumn SecurityStatus =
\t\tSWITCH(TRUE(), [HasSensitivityLabel] && [IsLabelEncrypted], "Protected", [IsLabelEncrypted], "Encrypted Only", [HasSensitivityLabel], "Labeled Only", "Unprotected")
\t\tdataType: string
\t\tlineageTag: c1a00002-0001-0001-0001-000000000203
\t\tsummarizeBy: none

\t\tannotation SummarizationSetBy = Automatic

\tcolumn HasSensitivityLabel = NOT(ISBLANK([SensitivityLabelInfo.Id]))
\t\tdataType: boolean
\t\tlineageTag: c1a00002-0001-0001-0001-000000000204
\t\tsummarizeBy: none
\t\tformatString: """TRUE"";""TRUE"";""FALSE"""

\t\tannotation SummarizationSetBy = Automatic

\tcolumn FileAgeCategory = SWITCH(TRUE(), DATEDIFF([TimeCreated], TODAY(), DAY) < 30, "New", DATEDIFF([TimeCreated], TODAY(), DAY) < 90, "Recent", DATEDIFF([TimeCreated], TODAY(), DAY) < 365, "Standard", DATEDIFF([TimeCreated], TODAY(), DAY) < 730, "Old", "Ancient")
\t\tdataType: string
\t\tlineageTag: c1a00002-0001-0001-0001-000000000205
\t\tsummarizeBy: none

\t\tannotation SummarizationSetBy = Automatic

\tcolumn IsLargeFile = [SizeInBytes] > 104857600
\t\tdataType: boolean
\t\tlineageTag: c1a00002-0001-0001-0001-000000000206
\t\tsummarizeBy: none
\t\tformatString: """TRUE"";""TRUE"";""FALSE"""

\t\tannotation SummarizationSetBy = Automatic

\tcolumn VersionBloatRatio = DIVIDE([SizeInBytesWithVersions], [SizeInBytes], 0)
\t\tdataType: double
\t\tlineageTag: c1a00002-0001-0001-0001-000000000207
\t\tsummarizeBy: none
\t\tformatString: #,0.00

\t\tannotation SummarizationSetBy = Automatic

\tcolumn DaysSinceModified = DATEDIFF([TimeLastModified], TODAY(), DAY)
\t\tdataType: int64
\t\tlineageTag: c1a00002-0001-0001-0001-000000000208
\t\tsummarizeBy: none

\t\tannotation SummarizationSetBy = Automatic

\tcolumn IsStale = [DaysSinceModified] > 180
\t\tdataType: boolean
\t\tlineageTag: c1a00002-0001-0001-0001-000000000209
\t\tsummarizeBy: none
\t\tformatString: """TRUE"";""TRUE"";""FALSE"""

\t\tannotation SummarizationSetBy = Automatic

\tcolumn FileRiskScore =
\t\tVAR _NoLabel = IF(ISBLANK([SensitivityLabelInfo.Id]), 30, 0)
\t\tVAR _NoEncryption = IF(NOT([IsLabelEncrypted]), 20, 0)
\t\tVAR _Stale = IF(DATEDIFF([TimeLastModified], TODAY(), DAY) > 180, 15, 0)
\t\tVAR _LargeFile = IF([SizeInBytes] > 104857600, 10, 0)
\t\tVAR _VersionBloat = IF(DIVIDE([SizeInBytesWithVersions], [SizeInBytes], 0) > 10, 15, 0)
\t\tVAR _ExternalPath = IF(CONTAINSSTRING([DirName], "/External/") || CONTAINSSTRING([DirName], "/Shared with Everyone/"), 10, 0)
\t\tRETURN _NoLabel + _NoEncryption + _Stale + _LargeFile + _VersionBloat + _ExternalPath
\t\tdataType: int64
\t\tlineageTag: c1a00002-0001-0001-0001-000000000210
\t\tsummarizeBy: none

\t\tannotation SummarizationSetBy = Automatic
''',
    'SPOFileActions': '''\
\tcolumn ActionHour = HOUR([ActionDate])
\t\tdataType: int64
\t\tlineageTag: a1b2c3d4-e5f6-7890-abcd-ef1234567821
\t\tsummarizeBy: none

\t\tannotation SummarizationSetBy = Automatic

\tcolumn IsWeekend = WEEKDAY([ActionDate], 2) > 5
\t\tdataType: boolean
\t\tformatString: """TRUE"";""TRUE"";""FALSE"""
\t\tlineageTag: a1b2c3d4-e5f6-7890-abcd-ef1234567822
\t\tsummarizeBy: none

\t\tannotation SummarizationSetBy = Automatic

\tcolumn IsAfterHours = OR(HOUR([ActionDate]) < 7, HOUR([ActionDate]) > 19)
\t\tdataType: boolean
\t\tformatString: """TRUE"";""TRUE"";""FALSE"""
\t\tlineageTag: a1b2c3d4-e5f6-7890-abcd-ef1234567823
\t\tsummarizeBy: none

\t\tannotation SummarizationSetBy = Automatic

\tcolumn IsHighRiskAction = [ActionName] IN {"FileDeleted", "PermissionChanged", "SharingSet", "FileVersionsAllDeleted", "FileMalwareDetected"}
\t\tdataType: boolean
\t\tformatString: """TRUE"";""TRUE"";""FALSE"""
\t\tlineageTag: a1b2c3d4-e5f6-7890-abcd-ef1234567824
\t\tsummarizeBy: none

\t\tannotation SummarizationSetBy = Automatic

\tcolumn IsExternalUser = [ActorType] = "External"
\t\tdataType: boolean
\t\tformatString: """TRUE"";""TRUE"";""FALSE"""
\t\tlineageTag: a1b2c3d4-e5f6-7890-abcd-ef1234567840
\t\tsummarizeBy: none

\t\tannotation SummarizationSetBy = Automatic

\tcolumn IsSuspiciousActivity = [IsAfterHours] && [IsExternalUser] && [IsHighRiskAction]
\t\tdataType: boolean
\t\tformatString: """TRUE"";""TRUE"";""FALSE"""
\t\tlineageTag: a1b2c3d4-e5f6-7890-abcd-ef1234567825
\t\tsummarizeBy: none

\t\tannotation SummarizationSetBy = Automatic

\tcolumn ActionCategory =
\t\t\tSWITCH(
\t\t\t\tTRUE(),
\t\t\t\t[ActionName] IN {"FileAccessed", "FileCheckedOut"}, "Read",
\t\t\t\t[ActionName] IN {"FileModified", "FileUploaded", "FileRenamed", "FileMoved", "FileCheckedIn"}, "Write",
\t\t\t\t[ActionName] IN {"FileDeleted", "FileVersionsAllDeleted"}, "Delete",
\t\t\t\t"Manage"
\t\t\t)
\t\tdataType: string
\t\tlineageTag: a1b2c3d4-e5f6-7890-abcd-ef1234567826
\t\tsummarizeBy: none

\t\tannotation SummarizationSetBy = Automatic

\tcolumn UserAgentCategory =
\t\t\tSWITCH(
\t\t\t\tTRUE(),
\t\t\t\tCONTAINSSTRING([UserAgent], "Teams"), "Teams",
\t\t\t\tCONTAINSSTRING([UserAgent], "OneDrive"), "OneDrive",
\t\t\t\tCONTAINSSTRING([UserAgent], "Mozilla") || CONTAINSSTRING([UserAgent], "Chrome") || CONTAINSSTRING([UserAgent], "Edge"), "Browser",
\t\t\t\tCONTAINSSTRING([UserAgent], "Mobile") || CONTAINSSTRING([UserAgent], "Android") || CONTAINSSTRING([UserAgent], "iOS"), "Mobile",
\t\t\t\tCONTAINSSTRING([UserAgent], "CSOM") || CONTAINSSTRING([UserAgent], "Microsoft Office"), "API",
\t\t\t\t"Other"
\t\t\t)
\t\tdataType: string
\t\tlineageTag: a1b2c3d4-e5f6-7890-abcd-ef1234567827
\t\tsummarizeBy: none

\t\tannotation SummarizationSetBy = Automatic

\tcolumn IsExternalDownload = [IsExternalUser] && [ActionName] = "FileAccessed"
\t\tdataType: boolean
\t\tformatString: """TRUE"";""TRUE"";""FALSE"""
\t\tlineageTag: a1b2c3d4-e5f6-7890-abcd-ef1234567828
\t\tsummarizeBy: none

\t\tannotation SummarizationSetBy = Automatic

\tcolumn TimePeriod =
\t\t\tSWITCH(
\t\t\t\tTRUE(),
\t\t\t\t[ActionHour] >= 6 && [ActionHour] < 12, "Morning",
\t\t\t\t[ActionHour] >= 12 && [ActionHour] < 17, "Afternoon",
\t\t\t\t[ActionHour] >= 17 && [ActionHour] < 21, "Evening",
\t\t\t\t"Night"
\t\t\t)
\t\tdataType: string
\t\tlineageTag: a1b2c3d4-e5f6-7890-abcd-ef1234567829
\t\tsummarizeBy: none

\t\tannotation SummarizationSetBy = Automatic
''',
    'SPOPermissions': '''\
\tcolumn IsAnonymousLink = [LinkScope] = "Anyone"
\t\tdataType: boolean
\t\tformatString: """TRUE"";""TRUE"";""FALSE"""
\t\tlineageTag: b2c3d4e5-f6a7-8901-bcde-f12345678920
\t\tsummarizeBy: none

\t\tannotation SummarizationSetBy = Automatic

\tcolumn IsExternalShare = [LinkScope] = "Anyone"
\t\tdataType: boolean
\t\tformatString: """TRUE"";""TRUE"";""FALSE"""
\t\tlineageTag: b2c3d4e5-f6a7-8901-bcde-f12345678921
\t\tsummarizeBy: none

\t\tannotation SummarizationSetBy = Automatic

\tcolumn HasNoExpiration = ISBLANK([ShareExpirationTime])
\t\tdataType: boolean
\t\tformatString: """TRUE"";""TRUE"";""FALSE"""
\t\tlineageTag: b2c3d4e5-f6a7-8901-bcde-f12345678922
\t\tsummarizeBy: none

\t\tannotation SummarizationSetBy = Automatic

\tcolumn PermissionRiskLevel =
\t\t\tSWITCH(
\t\t\t\tTRUE(),
\t\t\t\t[IsAnonymousLink] && [RoleDefinition] IN {"Write", "Full Control"}, "Critical",
\t\t\t\t[IsAnonymousLink], "High",
\t\t\t\t[IsExternalShare] && [HasNoExpiration], "High",
\t\t\t\t[IsExternalShare], "Medium",
\t\t\t\t"Low"
\t\t\t)
\t\tdataType: string
\t\tlineageTag: b2c3d4e5-f6a7-8901-bcde-f12345678923
\t\tsummarizeBy: none

\t\tannotation SummarizationSetBy = Automatic

\tcolumn PermissionRiskScore = SWITCH([PermissionRiskLevel], "Critical", 100, "High", 75, "Medium", 50, 25)
\t\tdataType: int64
\t\tlineageTag: b2c3d4e5-f6a7-8901-bcde-f12345678924
\t\tsummarizeBy: none

\t\tannotation SummarizationSetBy = Automatic

\tcolumn IsOverprivileged = [RoleDefinition] IN {"Full Control", "Write"} && [IsAnonymousLink]
\t\tdataType: boolean
\t\tformatString: """TRUE"";""TRUE"";""FALSE"""
\t\tlineageTag: b2c3d4e5-f6a7-8901-bcde-f12345678925
\t\tsummarizeBy: none

\t\tannotation SummarizationSetBy = Automatic

\tcolumn PermissionAgeCategory =
\t\t\tSWITCH(
\t\t\t\tTRUE(),
\t\t\t\tDATEDIFF([ShareCreatedTime], TODAY(), DAY) < 30, "New",
\t\t\t\tDATEDIFF([ShareCreatedTime], TODAY(), DAY) < 90, "Recent",
\t\t\t\tDATEDIFF([ShareCreatedTime], TODAY(), DAY) < 365, "Standard",
\t\t\t\tDATEDIFF([ShareCreatedTime], TODAY(), DAY) < 730, "Old",
\t\t\t\t"Ancient"
\t\t\t)
\t\tdataType: string
\t\tlineageTag: b2c3d4e5-f6a7-8901-bcde-f12345678926
\t\tsummarizeBy: none

\t\tannotation SummarizationSetBy = Automatic

\tcolumn PermissionAgeDays = DATEDIFF([ShareCreatedTime], TODAY(), DAY)
\t\tdataType: int64
\t\tlineageTag: b2c3d4e5-f6a7-8901-bcde-f12345678927
\t\tsummarizeBy: none

\t\tannotation SummarizationSetBy = Automatic

\tcolumn DaysUntilExpiry = IF(ISBLANK([ShareExpirationTime]), BLANK(), DATEDIFF(TODAY(), [ShareExpirationTime], DAY))
\t\tdataType: int64
\t\tlineageTag: b2c3d4e5-f6a7-8901-bcde-f12345678928
\t\tsummarizeBy: none

\t\tannotation SummarizationSetBy = Automatic

\tcolumn IsExpiringSoon = NOT(ISBLANK([ShareExpirationTime])) && [DaysUntilExpiry] <= 30 && [DaysUntilExpiry] > 0
\t\tdataType: boolean
\t\tformatString: """TRUE"";""TRUE"";""FALSE"""
\t\tlineageTag: b2c3d4e5-f6a7-8901-bcde-f12345678929
\t\tsummarizeBy: none

\t\tannotation SummarizationSetBy = Automatic

\tcolumn LinkCategory = IF(ISBLANK([LinkScope]), "Direct", [LinkScope])
\t\tdataType: string
\t\tlineageTag: b2c3d4e5-f6a7-8901-bcde-f1234567892a
\t\tsummarizeBy: none

\t\tannotation SummarizationSetBy = Automatic
''',
    'SPOGroups': '''\
\tcolumn IsOwnerless = ISBLANK([Owner.Email])
\t\tdataType: boolean
\t\tformatString: """TRUE"";""TRUE"";""FALSE"""
\t\tlineageTag: c3d4e5f6-a7b8-9012-cdef-123456789020
\t\tsummarizeBy: none

\t\tannotation SummarizationSetBy = Automatic

\tcolumn GroupRiskLevel =
\t\t\tSWITCH(
\t\t\t\tTRUE(),
\t\t\t\t[IsOwnerless] && [GroupType] = "SecurityGroup", "Critical",
\t\t\t\t[IsOwnerless], "High",
\t\t\t\t"Low"
\t\t\t)
\t\tdataType: string
\t\tlineageTag: c3d4e5f6-a7b8-9012-cdef-123456789023
\t\tsummarizeBy: none

\t\tannotation SummarizationSetBy = Automatic
''',
}

# ============================================================
# Relationships for model.tmdl
# ============================================================

RELATIONSHIPS = """\

relationship 9c3a7b1e-4d2f-4a8e-b6c1-d5e7f9a0b2c4
\tfromColumn: SPOFiles.SiteId
\ttoColumn: SPOSites.Id

relationship a4b8c2d6-5e3f-4b9a-c7d1-e6f0a1b3c5d7
\tfromColumn: SPOFileActions.SiteId
\ttoColumn: SPOSites.Id

relationship b5c9d3e7-6f4a-4c0b-d8e2-f7a1b2c4d6e8
\tfromColumn: SPOPermissions.SiteId
\ttoColumn: SPOSites.Id

relationship c6d0e4f8-7a5b-4d1c-e9f3-a8b2c3d5e7f9
\tfromColumn: SPOGroups.SiteId
\ttoColumn: SPOSites.Id

relationship d7e1f5a9-8b6c-4e2d-f0a4-b9c3d4e6f8a0
\tisActive: false
\tfromColumn: SPOFileActions.ListItemId
\ttoColumn: SPOFiles.ItemId

relationship e8f2a6b0-9c7d-4f3e-a1b5-c0d4e5f7a9b1
\tisActive: false
\tfromColumn: SPOPermissions.ListItemId
\ttoColumn: SPOFiles.ItemId
"""

# ============================================================
# Complete _Measures.tmdl content
# ============================================================

MEASURES_TMDL = r"""table _Measures
	lineageTag: m1a00000-0000-0000-0001-000000000001

	measure 'Total Sites' =
			COUNTROWS(SPOSites)
		formatString: #,##0
		displayFolder: Executive Overview
		lineageTag: m1a00101-0001-0001-0001-000000000001

	measure 'Total Files' =
			COUNTROWS(SPOFiles)
		formatString: #,##0
		displayFolder: Executive Overview
		lineageTag: m1a00101-0001-0001-0001-000000000002

	measure 'Total Storage TB' =
			DIVIDE(SUM(SPOFiles[SizeInBytes]), 1099511627776, 0)
		formatString: 0.00
		displayFolder: Executive Overview
		lineageTag: m1a00101-0001-0001-0001-000000000003

	measure 'Total Users' =
			DISTINCTCOUNT(SPOFileActions[ActorEmail])
		formatString: #,##0
		displayFolder: Executive Overview
		lineageTag: m1a00101-0001-0001-0001-000000000004

	measure 'Security Score' =
			VAR SharingRisk = DIVIDE(CALCULATE(COUNTROWS(SPOPermissions), SPOPermissions[IsAnonymousLink] = TRUE()), COUNTROWS(SPOPermissions), 0)
			VAR LabelCoverage = DIVIDE(CALCULATE(COUNTROWS(SPOFiles), SPOFiles[HasSensitivityLabel] = TRUE()), COUNTROWS(SPOFiles), 0)
			VAR PermRisk = DIVIDE(CALCULATE(COUNTROWS(SPOPermissions), SPOPermissions[PermissionRiskLevel] IN {"Critical", "High"}), COUNTROWS(SPOPermissions), 0)
			RETURN (1 - SharingRisk * 0.35 - (1 - LabelCoverage) * 0.20 - PermRisk * 0.25) * 100
		formatString: 0.0
		displayFolder: Executive Overview
		lineageTag: m1a00101-0001-0001-0001-000000000005

	measure 'Security Grade' =
			VAR Score = [Security Score]
			RETURN SWITCH(TRUE(), Score >= 90, "A", Score >= 80, "B", Score >= 70, "C", Score >= 60, "D", "F")
		displayFolder: Executive Overview
		lineageTag: m1a00101-0001-0001-0001-000000000006

	measure 'Critical Risk Sites' =
			CALCULATE(COUNTROWS(SPOSites), SPOSites[SiteRiskTier] = "Critical")
		formatString: #,##0
		displayFolder: Executive Overview
		lineageTag: m1a00101-0001-0001-0001-000000000007

	measure 'High Risk Sites' =
			CALCULATE(COUNTROWS(SPOSites), SPOSites[SiteRiskTier] = "High")
		formatString: #,##0
		displayFolder: Executive Overview
		lineageTag: m1a00101-0001-0001-0001-000000000008

	measure 'Total Actions' =
			COUNTROWS(SPOFileActions)
		formatString: #,##0
		displayFolder: Executive Overview
		lineageTag: m1a00101-0001-0001-0001-000000000009

	measure 'Avg Site Risk Score' =
			AVERAGE(SPOSites[CalcSiteRiskScore])
		formatString: 0.0
		displayFolder: Executive Overview
		lineageTag: m1a00101-0001-0001-0001-000000000010

	measure 'Sites External Sharing' =
			CALCULATE(COUNTROWS(SPOSites), SPOSites[IsExternalSharingEnabled] = TRUE())
		formatString: #,##0
		displayFolder: Executive Overview
		lineageTag: m1a00101-0001-0001-0001-000000000011

	measure 'Total Permissions' =
			COUNTROWS(SPOPermissions)
		formatString: #,##0
		displayFolder: Executive Overview
		lineageTag: m1a00101-0001-0001-0001-000000000012

	measure 'Anonymous Links' =
			CALCULATE(COUNTROWS(SPOPermissions), SPOPermissions[IsAnonymousLink] = TRUE())
		formatString: #,##0
		displayFolder: External Sharing
		lineageTag: m1a00201-0002-0002-0002-000000000001

	measure 'Organization Links' =
			CALCULATE(COUNTROWS(SPOPermissions), SPOPermissions[LinkScope] = "Organization")
		formatString: #,##0
		displayFolder: External Sharing
		lineageTag: m1a00201-0002-0002-0002-000000000002

	measure 'External Shares' =
			CALCULATE(COUNTROWS(SPOPermissions), SPOPermissions[IsExternalShare] = TRUE())
		formatString: #,##0
		displayFolder: External Sharing
		lineageTag: m1a00201-0002-0002-0002-000000000003

	measure 'Direct Access Permissions' =
			CALCULATE(COUNTROWS(SPOPermissions), ISBLANK(SPOPermissions[LinkScope]))
		formatString: #,##0
		displayFolder: External Sharing
		lineageTag: m1a00201-0002-0002-0002-000000000004

	measure 'Never Expiring Links' =
			CALCULATE(COUNTROWS(SPOPermissions), SPOPermissions[HasNoExpiration] = TRUE(), NOT(ISBLANK(SPOPermissions[LinkCategory])), SPOPermissions[LinkCategory] <> "Direct")
		formatString: #,##0
		displayFolder: External Sharing
		lineageTag: m1a00201-0002-0002-0002-000000000005

	measure 'Anonymous Write Links' =
			CALCULATE(COUNTROWS(SPOPermissions), SPOPermissions[IsAnonymousLink] = TRUE(), SPOPermissions[RoleDefinition] IN {"Write", "Full Control", "Contribute", "Edit"})
		formatString: #,##0
		displayFolder: External Sharing
		lineageTag: m1a00201-0002-0002-0002-000000000006

	measure 'Oversharing Risk Score' =
			VAR AnonPct = DIVIDE([Anonymous Links], [Total Permissions], 0)
			VAR ExtPct = DIVIDE([External Shares], [Total Permissions], 0)
			VAR NoExpiryPct = DIVIDE([Never Expiring Links], [Total Permissions], 0)
			RETURN (AnonPct * 40 + ExtPct * 30 + NoExpiryPct * 30) * 100
		formatString: 0.0
		displayFolder: External Sharing
		lineageTag: m1a00201-0002-0002-0002-000000000007

	measure 'Sites with Anyone Links' =
			CALCULATE(DISTINCTCOUNT(SPOPermissions[SiteId]), SPOPermissions[LinkScope] = "Anyone")
		formatString: #,##0
		displayFolder: External Sharing
		lineageTag: m1a00201-0002-0002-0002-000000000008

	measure 'Avg Links Per File' =
			DIVIDE(CALCULATE(COUNTROWS(SPOPermissions), NOT(ISBLANK(SPOPermissions[LinkCategory])), SPOPermissions[LinkCategory] <> "Direct"), COUNTROWS(SPOFiles), 0)
		formatString: 0.00
		displayFolder: External Sharing
		lineageTag: m1a00201-0002-0002-0002-000000000009

	measure 'External Link Users' =
			CALCULATE(SUM(SPOPermissions[TotalUserCount]), SPOPermissions[LinkScope] = "Anyone")
		formatString: #,##0
		displayFolder: External Sharing
		lineageTag: m1a00201-0002-0002-0002-000000000010

	measure 'Files with Anonymous Access' =
			CALCULATE(DISTINCTCOUNT(SPOPermissions[ListItemId]), SPOPermissions[IsAnonymousLink] = TRUE())
		formatString: #,##0
		displayFolder: External Sharing
		lineageTag: m1a00201-0002-0002-0002-000000000011

	measure 'External Share Pct' =
			DIVIDE([External Shares], [Total Permissions], 0) * 100
		formatString: 0.0"%"
		displayFolder: External Sharing
		lineageTag: m1a00201-0002-0002-0002-000000000012

	measure 'Anonymous Link Pct' =
			DIVIDE([Anonymous Links], [Total Permissions], 0) * 100
		formatString: 0.0"%"
		displayFolder: External Sharing
		lineageTag: m1a00201-0002-0002-0002-000000000013

	measure 'High Risk Sharing Sites' =
			CALCULATE(DISTINCTCOUNT(SPOPermissions[SiteId]), SPOPermissions[PermissionRiskLevel] IN {"Critical", "High"})
		formatString: #,##0
		displayFolder: External Sharing
		lineageTag: m1a00201-0002-0002-0002-000000000014

	measure 'Critical Risk Permissions' =
			CALCULATE(COUNTROWS(SPOPermissions), SPOPermissions[PermissionRiskLevel] = "Critical")
		formatString: #,##0
		displayFolder: Permission Analysis
		lineageTag: m1a00301-0003-0003-0003-000000000001

	measure 'High Risk Permissions' =
			CALCULATE(COUNTROWS(SPOPermissions), SPOPermissions[PermissionRiskLevel] = "High")
		formatString: #,##0
		displayFolder: Permission Analysis
		lineageTag: m1a00301-0003-0003-0003-000000000002

	measure 'Medium Risk Permissions' =
			CALCULATE(COUNTROWS(SPOPermissions), SPOPermissions[PermissionRiskLevel] = "Medium")
		formatString: #,##0
		displayFolder: Permission Analysis
		lineageTag: m1a00301-0003-0003-0003-000000000003

	measure 'Low Risk Permissions' =
			CALCULATE(COUNTROWS(SPOPermissions), SPOPermissions[PermissionRiskLevel] = "Low")
		formatString: #,##0
		displayFolder: Permission Analysis
		lineageTag: m1a00301-0003-0003-0003-000000000004

	measure 'Overprivileged Users' =
			CALCULATE(COUNTROWS(SPOPermissions), SPOPermissions[IsOverprivileged] = TRUE())
		formatString: #,##0
		displayFolder: Permission Analysis
		lineageTag: m1a00301-0003-0003-0003-000000000005

	measure 'Avg Permissions Per File' =
			DIVIDE(COUNTROWS(SPOPermissions), DISTINCTCOUNT(SPOPermissions[ListItemId]), 0)
		formatString: 0.0
		displayFolder: Permission Analysis
		lineageTag: m1a00301-0003-0003-0003-000000000006

	measure 'Full Control Permissions' =
			CALCULATE(COUNTROWS(SPOPermissions), SPOPermissions[RoleDefinition] = "Full Control")
		formatString: #,##0
		displayFolder: Permission Analysis
		lineageTag: m1a00301-0003-0003-0003-000000000007

	measure 'Permission Sprawl Index' =
			DIVIDE(COUNTROWS(SPOPermissions), COUNTROWS(SPOSites), 0)
		formatString: 0.0
		displayFolder: Permission Analysis
		lineageTag: m1a00301-0003-0003-0003-000000000008

	measure 'Total Shared Users' =
			SUM(SPOPermissions[TotalUserCount])
		formatString: #,##0
		displayFolder: Permission Analysis
		lineageTag: m1a00301-0003-0003-0003-000000000009

	measure 'Specific People Links' =
			CALCULATE(COUNTROWS(SPOPermissions), SPOPermissions[LinkScope] = "SpecificPeople")
		formatString: #,##0
		displayFolder: Permission Analysis
		lineageTag: m1a00301-0003-0003-0003-000000000010

	measure 'File Permissions' =
			CALCULATE(COUNTROWS(SPOPermissions), SPOPermissions[ItemType] = "File")
		formatString: #,##0
		displayFolder: Permission Analysis
		lineageTag: m1a00301-0003-0003-0003-000000000011

	measure 'Folder Permissions' =
			CALCULATE(COUNTROWS(SPOPermissions), SPOPermissions[ItemType] = "Folder")
		formatString: #,##0
		displayFolder: Permission Analysis
		lineageTag: m1a00301-0003-0003-0003-000000000012

	measure 'Avg Users Per Permission' =
			DIVIDE(SUM(SPOPermissions[TotalUserCount]), COUNTROWS(SPOPermissions), 0)
		formatString: 0.0
		displayFolder: Permission Analysis
		lineageTag: m1a00301-0003-0003-0003-000000000013

	measure 'Avg Permission Risk Score' =
			AVERAGE(SPOPermissions[PermissionRiskScore])
		formatString: 0.0
		displayFolder: Permission Analysis
		lineageTag: m1a00301-0003-0003-0003-000000000014

	measure 'File Label Coverage Pct' =
			DIVIDE(CALCULATE(COUNTROWS(SPOFiles), SPOFiles[HasSensitivityLabel] = TRUE()), COUNTROWS(SPOFiles), 0) * 100
		formatString: 0.0
		displayFolder: Sensitivity & Encryption
		lineageTag: m1a00401-0004-0004-0004-000000000001

	measure 'Site Label Coverage Pct' =
			DIVIDE(CALCULATE(COUNTROWS(SPOSites), SPOSites[HasSensitivityLabel] = TRUE()), COUNTROWS(SPOSites), 0) * 100
		formatString: 0.0
		displayFolder: Sensitivity & Encryption
		lineageTag: m1a00401-0004-0004-0004-000000000002

	measure 'Encrypted Files' =
			CALCULATE(COUNTROWS(SPOFiles), SPOFiles[IsLabelEncrypted] = TRUE())
		formatString: #,##0
		displayFolder: Sensitivity & Encryption
		lineageTag: m1a00401-0004-0004-0004-000000000003

	measure 'Encrypted File Pct' =
			DIVIDE([Encrypted Files], COUNTROWS(SPOFiles), 0) * 100
		formatString: 0.0
		displayFolder: Sensitivity & Encryption
		lineageTag: m1a00401-0004-0004-0004-000000000004

	measure 'Unprotected Files' =
			CALCULATE(COUNTROWS(SPOFiles), SPOFiles[SecurityStatus] = "Unprotected")
		formatString: #,##0
		displayFolder: Sensitivity & Encryption
		lineageTag: m1a00401-0004-0004-0004-000000000005

	measure 'Unprotected Pct' =
			DIVIDE([Unprotected Files], COUNTROWS(SPOFiles), 0) * 100
		formatString: 0.0
		displayFolder: Sensitivity & Encryption
		lineageTag: m1a00401-0004-0004-0004-000000000006

	measure 'Protected Files' =
			CALCULATE(COUNTROWS(SPOFiles), SPOFiles[SecurityStatus] = "Protected")
		formatString: #,##0
		displayFolder: Sensitivity & Encryption
		lineageTag: m1a00401-0004-0004-0004-000000000007

	measure 'Labeled Only Files' =
			CALCULATE(COUNTROWS(SPOFiles), SPOFiles[SecurityStatus] = "Labeled Only")
		formatString: #,##0
		displayFolder: Sensitivity & Encryption
		lineageTag: m1a00401-0004-0004-0004-000000000008

	measure 'Encrypted Only Files' =
			CALCULATE(COUNTROWS(SPOFiles), SPOFiles[SecurityStatus] = "Encrypted Only")
		formatString: #,##0
		displayFolder: Sensitivity & Encryption
		lineageTag: m1a00401-0004-0004-0004-000000000009

	measure 'Sensitive Externally Shared' =
			CALCULATE(DISTINCTCOUNT(SPOPermissions[ListItemId]), FILTER(VALUES(SPOPermissions[ListItemId]), CALCULATE(MAX(SPOFiles[HasSensitivityLabel])) = TRUE()), SPOPermissions[IsExternalShare] = TRUE())
		formatString: #,##0
		displayFolder: Sensitivity & Encryption
		lineageTag: m1a00401-0004-0004-0004-000000000010

	measure 'Unlabeled Sites' =
			CALCULATE(COUNTROWS(SPOSites), SPOSites[HasSensitivityLabel] = FALSE())
		formatString: #,##0
		displayFolder: Sensitivity & Encryption
		lineageTag: m1a00401-0004-0004-0004-000000000011

	measure 'Label Gap Score' =
			(100 - [File Label Coverage Pct]) * 0.6 + (100 - [Site Label Coverage Pct]) * 0.4
		formatString: 0.0
		displayFolder: Sensitivity & Encryption
		lineageTag: m1a00401-0004-0004-0004-000000000012

	measure 'Total Downloads' =
			CALCULATE(COUNTROWS(SPOFileActions), SPOFileActions[ActionCategory] = "Read")
		formatString: #,##0
		displayFolder: User Activity
		lineageTag: m1a00501-0005-0005-0005-000000000001

	measure 'Total Uploads' =
			CALCULATE(COUNTROWS(SPOFileActions), SPOFileActions[ActionCategory] = "Write")
		formatString: #,##0
		displayFolder: User Activity
		lineageTag: m1a00501-0005-0005-0005-000000000002

	measure 'Total Deletes' =
			CALCULATE(COUNTROWS(SPOFileActions), SPOFileActions[ActionCategory] = "Delete")
		formatString: #,##0
		displayFolder: User Activity
		lineageTag: m1a00501-0005-0005-0005-000000000003

	measure 'Management Actions' =
			CALCULATE(COUNTROWS(SPOFileActions), SPOFileActions[ActionCategory] = "Manage")
		formatString: #,##0
		displayFolder: User Activity
		lineageTag: m1a00501-0005-0005-0005-000000000004

	measure 'After Hours Actions' =
			CALCULATE(COUNTROWS(SPOFileActions), SPOFileActions[IsAfterHours] = TRUE())
		formatString: #,##0
		displayFolder: User Activity
		lineageTag: m1a00501-0005-0005-0005-000000000005

	measure 'After Hours Pct' =
			DIVIDE([After Hours Actions], [Total Actions], 0) * 100
		formatString: 0.0
		displayFolder: User Activity
		lineageTag: m1a00501-0005-0005-0005-000000000006

	measure 'Weekend Actions' =
			CALCULATE(COUNTROWS(SPOFileActions), SPOFileActions[IsWeekend] = TRUE())
		formatString: #,##0
		displayFolder: User Activity
		lineageTag: m1a00501-0005-0005-0005-000000000007

	measure 'Weekend Pct' =
			DIVIDE([Weekend Actions], [Total Actions], 0) * 100
		formatString: 0.0
		displayFolder: User Activity
		lineageTag: m1a00501-0005-0005-0005-000000000008

	measure 'Suspicious Activities' =
			CALCULATE(COUNTROWS(SPOFileActions), SPOFileActions[IsSuspiciousActivity] = TRUE())
		formatString: #,##0
		displayFolder: User Activity
		lineageTag: m1a00501-0005-0005-0005-000000000009

	measure 'External User Downloads' =
			CALCULATE(COUNTROWS(SPOFileActions), SPOFileActions[IsExternalDownload] = TRUE())
		formatString: #,##0
		displayFolder: User Activity
		lineageTag: m1a00501-0005-0005-0005-000000000010

	measure 'Unique IPs' =
			DISTINCTCOUNT(SPOFileActions[ClientIP])
		formatString: #,##0
		displayFolder: User Activity
		lineageTag: m1a00501-0005-0005-0005-000000000011

	measure 'Avg Actions Per User' =
			DIVIDE([Total Actions], [Total Users], 0)
		formatString: 0.0
		displayFolder: User Activity
		lineageTag: m1a00501-0005-0005-0005-000000000012

	measure 'High Risk Actions' =
			CALCULATE(COUNTROWS(SPOFileActions), SPOFileActions[IsHighRiskAction] = TRUE())
		formatString: #,##0
		displayFolder: User Activity
		lineageTag: m1a00501-0005-0005-0005-000000000013

	measure 'Unique Active Users' =
			DISTINCTCOUNT(SPOFileActions[ActorEmail])
		formatString: #,##0
		displayFolder: User Activity
		lineageTag: m1a00501-0005-0005-0005-000000000014

	measure 'External User Actions' =
			CALCULATE(COUNTROWS(SPOFileActions), SPOFileActions[IsExternalUser] = TRUE())
		formatString: #,##0
		displayFolder: User Activity
		lineageTag: m1a00501-0005-0005-0005-000000000015

	measure 'External Action Pct' =
			DIVIDE([External User Actions], [Total Actions], 0) * 100
		formatString: 0.0
		displayFolder: User Activity
		lineageTag: m1a00501-0005-0005-0005-000000000016

	measure 'Sites No Device Policy' =
			CALCULATE(COUNTROWS(SPOSites), SPOSites[BlockAccessFromUnmanagedDevices] = FALSE())
		formatString: #,##0
		displayFolder: Site Security
		lineageTag: m1a00601-0006-0006-0006-000000000001

	measure 'Orphaned Sites' =
			CALCULATE(COUNTROWS(SPOSites), SPOSites[IsOrphaned] = TRUE())
		formatString: #,##0
		displayFolder: Site Security
		lineageTag: m1a00601-0006-0006-0006-000000000002

	measure 'Locked Sites' =
			CALCULATE(COUNTROWS(SPOSites), SPOSites[ReadLocked] = TRUE())
		formatString: #,##0
		displayFolder: Site Security
		lineageTag: m1a00601-0006-0006-0006-000000000003

	measure 'Teams Connected Sites' =
			CALCULATE(COUNTROWS(SPOSites), SPOSites[IsTeamsConnectedSite] = TRUE())
		formatString: #,##0
		displayFolder: Site Security
		lineageTag: m1a00601-0006-0006-0006-000000000004

	measure 'Avg Site Risk' =
			AVERAGE(SPOSites[CalcSiteRiskScore])
		formatString: 0.0
		displayFolder: Site Security
		lineageTag: m1a00601-0006-0006-0006-000000000005

	measure 'External Sharing Enabled Sites' =
			CALCULATE(COUNTROWS(SPOSites), SPOSites[IsExternalSharingEnabled] = TRUE())
		formatString: #,##0
		displayFolder: Site Security
		lineageTag: m1a00601-0006-0006-0006-000000000006

	measure 'Team Sites' =
			CALCULATE(COUNTROWS(SPOSites), SPOSites[SiteType] = "Team")
		formatString: #,##0
		displayFolder: Site Security
		lineageTag: m1a00601-0006-0006-0006-000000000007

	measure 'Communication Sites' =
			CALCULATE(COUNTROWS(SPOSites), SPOSites[SiteType] = "Communication")
		formatString: #,##0
		displayFolder: Site Security
		lineageTag: m1a00601-0006-0006-0006-000000000008

	measure 'Personal Sites' =
			CALCULATE(COUNTROWS(SPOSites), SPOSites[SiteType] = "Personal")
		formatString: #,##0
		displayFolder: Site Security
		lineageTag: m1a00601-0006-0006-0006-000000000009

	measure 'Overprovisioned Sites' =
			CALCULATE(COUNTROWS(SPOSites), SPOSites[IsOverprovisioned] = TRUE())
		formatString: #,##0
		displayFolder: Site Security
		lineageTag: m1a00601-0006-0006-0006-000000000010

	measure 'Total Groups' =
			COUNTROWS(SPOGroups)
		formatString: #,##0
		displayFolder: Group Risks
		lineageTag: m1a00701-0007-0007-0007-000000000001

	measure 'Security Groups' =
			CALCULATE(COUNTROWS(SPOGroups), SPOGroups[GroupType] = "SecurityGroup")
		formatString: #,##0
		displayFolder: Group Risks
		lineageTag: m1a00701-0007-0007-0007-000000000002

	measure 'Ownerless Groups' =
			CALCULATE(COUNTROWS(SPOGroups), SPOGroups[IsOwnerless] = TRUE())
		formatString: #,##0
		displayFolder: Group Risks
		lineageTag: m1a00701-0007-0007-0007-000000000003

	measure 'M365 Groups' =
			CALCULATE(COUNTROWS(SPOGroups), SPOGroups[GroupType] = "M365Group")
		formatString: #,##0
		displayFolder: Group Risks
		lineageTag: m1a00701-0007-0007-0007-000000000004

	measure 'SharePoint Groups' =
			CALCULATE(COUNTROWS(SPOGroups), SPOGroups[GroupType] = "SharePointGroup")
		formatString: #,##0
		displayFolder: Group Risks
		lineageTag: m1a00701-0007-0007-0007-000000000005

	measure 'Critical Risk Groups' =
			CALCULATE(COUNTROWS(SPOGroups), SPOGroups[GroupRiskLevel] = "Critical")
		formatString: #,##0
		displayFolder: Group Risks
		lineageTag: m1a00701-0007-0007-0007-000000000006

	measure 'Groups High Risk' =
			CALCULATE(COUNTROWS(SPOGroups), SPOGroups[GroupRiskLevel] IN {"Critical", "High"})
		formatString: #,##0
		displayFolder: Group Risks
		lineageTag: m1a00701-0007-0007-0007-000000000007

	measure 'High Risk Groups' =
			CALCULATE(COUNTROWS(SPOGroups), SPOGroups[GroupRiskLevel] = "High")
		formatString: #,##0
		displayFolder: Group Risks
		lineageTag: m1a00701-0007-0007-0007-000000000008

	measure 'Ownerless Pct' =
			DIVIDE([Ownerless Groups], [Total Groups], 0) * 100
		formatString: 0.0
		displayFolder: Group Risks
		lineageTag: m1a00701-0007-0007-0007-000000000009

	measure 'Unique Site Groups' =
			DISTINCTCOUNT(SPOGroups[SiteId])
		formatString: #,##0
		displayFolder: Group Risks
		lineageTag: m1a00701-0007-0007-0007-000000000010

	measure 'Avg Groups Per Site' =
			DIVIDE(COUNTROWS(SPOGroups), DISTINCTCOUNT(SPOGroups[SiteId]), 0)
		formatString: 0.0
		displayFolder: Group Risks
		lineageTag: m1a00701-0007-0007-0007-000000000011

	measure 'Total Version Storage TB' =
			DIVIDE(SUM(SPOFiles[SizeInBytesWithVersions]) - SUM(SPOFiles[SizeInBytes]), 1099511627776, 0)
		formatString: 0.00
		displayFolder: File Intelligence
		lineageTag: m1a00801-0008-0008-0008-000000000001

	measure 'Avg Version Bloat Ratio' =
			AVERAGE(SPOFiles[VersionBloatRatio])
		formatString: 0.0
		displayFolder: File Intelligence
		lineageTag: m1a00801-0008-0008-0008-000000000002

	measure 'Large Files' =
			CALCULATE(COUNTROWS(SPOFiles), SPOFiles[IsLargeFile] = TRUE())
		formatString: #,##0
		displayFolder: File Intelligence
		lineageTag: m1a00801-0008-0008-0008-000000000003

	measure 'Reclaimable Storage GB' =
			DIVIDE(SUMX(FILTER(SPOFiles, SPOFiles[VersionBloatRatio] > 5), [SizeInBytesWithVersions] - [SizeInBytes]), 1073741824, 0)
		formatString: 0.0
		displayFolder: File Intelligence
		lineageTag: m1a00801-0008-0008-0008-000000000004

	measure 'Unique File Types' =
			DISTINCTCOUNT(SPOFiles[Extension])
		formatString: #,##0
		displayFolder: File Intelligence
		lineageTag: m1a00801-0008-0008-0008-000000000005

	measure 'Avg File Size MB' =
			AVERAGE(SPOFiles[FileSizeMB])
		formatString: 0.00
		displayFolder: File Intelligence
		lineageTag: m1a00801-0008-0008-0008-000000000006

	measure 'Total Documents' =
			CALCULATE(COUNTROWS(SPOFiles), SPOFiles[FileCategory] = "Documents")
		formatString: #,##0
		displayFolder: File Intelligence
		lineageTag: m1a00801-0008-0008-0008-000000000007

	measure 'Total Spreadsheets' =
			CALCULATE(COUNTROWS(SPOFiles), SPOFiles[FileCategory] = "Spreadsheets")
		formatString: #,##0
		displayFolder: File Intelligence
		lineageTag: m1a00801-0008-0008-0008-000000000008

	measure 'Excessive Version Files' =
			CALCULATE(COUNTROWS(SPOFiles), SPOFiles[MajorVersion] > 100)
		formatString: #,##0
		displayFolder: File Intelligence
		lineageTag: m1a00801-0008-0008-0008-000000000009

	measure 'Avg Versions Per File' =
			AVERAGE(SPOFiles[MajorVersion])
		formatString: 0.0
		displayFolder: File Intelligence
		lineageTag: m1a00801-0008-0008-0008-000000000010

	measure 'Storage Efficiency Score' =
			100 - (DIVIDE(SUM(SPOFiles[SizeInBytesWithVersions]) - SUM(SPOFiles[SizeInBytes]), SUM(SPOFiles[SizeInBytesWithVersions]), 0) * 100)
		formatString: 0.0
		displayFolder: File Intelligence
		lineageTag: m1a00801-0008-0008-0008-000000000011

	measure 'Stale Files' =
			CALCULATE(COUNTROWS(SPOFiles), SPOFiles[IsStale] = TRUE())
		formatString: #,##0
		displayFolder: Stale Access
		lineageTag: m1a00901-0009-0009-0009-000000000001

	measure 'Stale File Pct' =
			DIVIDE([Stale Files], COUNTROWS(SPOFiles), 0) * 100
		formatString: 0.0
		displayFolder: Stale Access
		lineageTag: m1a00901-0009-0009-0009-000000000002

	measure 'Stale Sites' =
			CALCULATE(COUNTROWS(SPOSites), SPOSites[DaysSinceModified] > 180)
		formatString: #,##0
		displayFolder: Stale Access
		lineageTag: m1a00901-0009-0009-0009-000000000003

	measure 'Abandoned Sites' =
			CALCULATE(COUNTROWS(SPOSites), SPOSites[DaysSinceModified] > 365)
		formatString: #,##0
		displayFolder: Stale Access
		lineageTag: m1a00901-0009-0009-0009-000000000004

	measure 'Ancient Permissions' =
			CALCULATE(COUNTROWS(SPOPermissions), SPOPermissions[PermissionAgeCategory] = "Ancient")
		formatString: #,##0
		displayFolder: Stale Access
		lineageTag: m1a00901-0009-0009-0009-000000000005

	measure 'Zombie Links' =
			CALCULATE(COUNTROWS(SPOPermissions), SPOPermissions[HasNoExpiration] = TRUE(), SPOPermissions[PermissionAgeDays] > 365, NOT(ISBLANK(SPOPermissions[LinkCategory])), SPOPermissions[LinkCategory] <> "Direct")
		formatString: #,##0
		displayFolder: Stale Access
		lineageTag: m1a00901-0009-0009-0009-000000000006

	measure 'Stale Permission Pct' =
			DIVIDE(CALCULATE(COUNTROWS(SPOPermissions), SPOPermissions[PermissionAgeCategory] IN {"Old", "Ancient"}), [Total Permissions], 0) * 100
		formatString: 0.0
		displayFolder: Stale Access
		lineageTag: m1a00901-0009-0009-0009-000000000007

	measure 'Stale Storage TB' =
			DIVIDE(CALCULATE(SUM(SPOFiles[SizeInBytes]), SPOFiles[IsStale] = TRUE()), 1099511627776, 0)
		formatString: 0.00
		displayFolder: Stale Access
		lineageTag: m1a00901-0009-0009-0009-000000000008

	measure 'Abandoned File Pct' =
			DIVIDE(CALCULATE(COUNTROWS(SPOFiles), SPOFiles[DaysSinceModified] > 365), COUNTROWS(SPOFiles), 0) * 100
		formatString: 0.0
		displayFolder: Stale Access
		lineageTag: m1a00901-0009-0009-0009-000000000009

	measure 'Avg Permission Age Days' =
			AVERAGEX(SPOPermissions, SPOPermissions[PermissionAgeDays])
		formatString: 0
		displayFolder: Stale Access
		lineageTag: m1a00901-0009-0009-0009-000000000010

	measure 'Sharing Risk Component' =
			VAR AnonPct = DIVIDE(CALCULATE(COUNTROWS(SPOPermissions), SPOPermissions[IsAnonymousLink] = TRUE()), COUNTROWS(SPOPermissions), 0)
			VAR ExtPct = DIVIDE(CALCULATE(COUNTROWS(SPOPermissions), SPOPermissions[IsExternalShare] = TRUE()), COUNTROWS(SPOPermissions), 0)
			RETURN (AnonPct * 60 + ExtPct * 40) * 100
		formatString: 0.0
		displayFolder: Risk Scoring
		lineageTag: m1a01001-0010-0010-0010-000000000001

	measure 'Permission Risk Component' =
			VAR CritPct = DIVIDE(CALCULATE(COUNTROWS(SPOPermissions), SPOPermissions[PermissionRiskLevel] = "Critical"), COUNTROWS(SPOPermissions), 0)
			VAR HighPct = DIVIDE(CALCULATE(COUNTROWS(SPOPermissions), SPOPermissions[PermissionRiskLevel] = "High"), COUNTROWS(SPOPermissions), 0)
			RETURN (CritPct * 70 + HighPct * 30) * 100
		formatString: 0.0
		displayFolder: Risk Scoring
		lineageTag: m1a01001-0010-0010-0010-000000000002

	measure 'Label Risk Component' =
			100 - [File Label Coverage Pct]
		formatString: 0.0
		displayFolder: Risk Scoring
		lineageTag: m1a01001-0010-0010-0010-000000000003

	measure 'Stale Risk Component' =
			[Stale File Pct]
		formatString: 0.0
		displayFolder: Risk Scoring
		lineageTag: m1a01001-0010-0010-0010-000000000004

	measure 'Group Risk Component' =
			DIVIDE(CALCULATE(COUNTROWS(SPOGroups), SPOGroups[GroupRiskLevel] IN {"Critical", "High"}), COUNTROWS(SPOGroups), 0) * 100
		formatString: 0.0
		displayFolder: Risk Scoring
		lineageTag: m1a01001-0010-0010-0010-000000000005

	measure 'Composite Risk Index' =
			[Sharing Risk Component] * 0.35 + [Permission Risk Component] * 0.25 + [Label Risk Component] * 0.20 + [Stale Risk Component] * 0.10 + [Group Risk Component] * 0.10
		formatString: 0.0
		displayFolder: Risk Scoring
		lineageTag: m1a01001-0010-0010-0010-000000000006

	measure 'Data Exposure Score' =
			VAR AnonFiles = CALCULATE(DISTINCTCOUNT(SPOPermissions[ListItemId]), SPOPermissions[IsAnonymousLink] = TRUE())
			VAR ExtFiles = CALCULATE(DISTINCTCOUNT(SPOPermissions[ListItemId]), SPOPermissions[IsExternalShare] = TRUE())
			VAR TotalFiles = COUNTROWS(SPOFiles)
			RETURN DIVIDE(AnonFiles * 3 + ExtFiles, TotalFiles, 0) * 100
		formatString: 0.0
		displayFolder: Risk Scoring
		lineageTag: m1a01001-0010-0010-0010-000000000007

	measure 'Risk Reduction Opportunities' =
			CALCULATE(COUNTROWS(SPOPermissions), SPOPermissions[IsAnonymousLink] = TRUE(), SPOPermissions[HasNoExpiration] = TRUE()) + CALCULATE(COUNTROWS(SPOFiles), SPOFiles[SecurityStatus] = "Unprotected", SPOFiles[IsStale] = TRUE()) + CALCULATE(COUNTROWS(SPOGroups), SPOGroups[IsOwnerless] = TRUE())
		formatString: #,##0
		displayFolder: Risk Scoring
		lineageTag: m1a01001-0010-0010-0010-000000000008

	measure 'Sites Above Threshold' =
			CALCULATE(COUNTROWS(SPOSites), SPOSites[CalcSiteRiskScore] >= 50)
		formatString: #,##0
		displayFolder: Risk Scoring
		lineageTag: m1a01001-0010-0010-0010-000000000009

	measure 'Avg Composite Risk' =
			AVERAGE(SPOSites[CalcSiteRiskScore])
		formatString: 0.0
		displayFolder: Risk Scoring
		lineageTag: m1a01001-0010-0010-0010-000000000010

	partition _Measures = calculated
		source = ROW("x", 1)
""".lstrip()


def patch_table(table_name):
    """Insert calculated columns into a table TMDL file before the partition block."""
    path = os.path.join(TABLES, f'{table_name}.tmdl')
    if not os.path.exists(path):
        print(f"  SKIP: {path} not found")
        return False

    content = open(path, 'r', encoding='utf-8').read()
    calc_cols = CALC_COLS[table_name]

    # Check if calculated columns already exist (check for a unique one)
    first_col_line = calc_cols.strip().split('\n')[0]
    # Extract column name: "	column Foo = ..." -> "Foo"
    col_match = re.search(r'column\s+(\w+)', first_col_line)
    if col_match and col_match.group(1) in content:
        print(f"  SKIP: {table_name} already has calculated columns")
        return False

    # Find the partition line and insert before it
    partition_match = re.search(r'\n(\tpartition\s+)', content)
    if partition_match:
        insert_pos = partition_match.start()
        new_content = content[:insert_pos] + '\n' + calc_cols.rstrip('\n') + '\n' + content[insert_pos:]
    else:
        # No partition found, append to end
        new_content = content.rstrip('\n') + '\n\n' + calc_cols
        print(f"  WARN: No partition found in {table_name}, appending to end")

    open(path, 'w', encoding='utf-8', newline='\n').write(new_content)
    col_count = calc_cols.count('\tcolumn ')
    print(f"  OK: {table_name} - added {col_count} calculated columns")
    return True


def create_measures():
    """Create _Measures.tmdl with all DAX measures."""
    path = os.path.join(TABLES, '_Measures.tmdl')
    if os.path.exists(path):
        content = open(path, 'r', encoding='utf-8').read()
        if 'Total Sites' in content and 'Composite Risk Index' in content:
            print("  SKIP: _Measures.tmdl already has all measures")
            return False

    open(path, 'w', encoding='utf-8', newline='\n').write(MEASURES_TMDL)
    print("  OK: Created _Measures.tmdl with 95 DAX measures")
    return True


def patch_model():
    """Add relationships and ref table _Measures to model.tmdl."""
    path = os.path.join(BASE, 'model.tmdl')
    if not os.path.exists(path):
        print(f"  SKIP: {path} not found")
        return False

    content = open(path, 'r', encoding='utf-8').read()
    changed = False

    # Add ref table _Measures if missing
    if 'ref table _Measures' not in content:
        # Find last ref table line and add after it
        last_ref_match = None
        for m in re.finditer(r'^ref table .+$', content, re.MULTILINE):
            last_ref_match = m
        if last_ref_match:
            insert_pos = last_ref_match.end()
            content = content[:insert_pos] + '\nref table _Measures' + content[insert_pos:]
            changed = True
            print("  OK: Added 'ref table _Measures'")
        else:
            print("  WARN: No 'ref table' lines found in model.tmdl")

    # Add relationships if missing
    if 'relationship 9c3a7b1e' not in content:
        content = content.rstrip('\n') + '\n' + RELATIONSHIPS
        changed = True
        print("  OK: Added 6 relationships")
    else:
        print("  SKIP: Relationships already exist")

    # Add _Measures to PBI_QueryOrder if present and missing
    if 'PBI_QueryOrder' in content and '_Measures' not in content:
        content = re.sub(
            r'(PBI_QueryOrder\s*=\s*\[.*?)"?\]',
            r'\1","_Measures"]',
            content
        )
        changed = True

    if changed:
        open(path, 'w', encoding='utf-8', newline='\n').write(content)
    return changed


def main():
    print("=" * 60)
    print("MGDC Security Dashboard - TMDL Patcher")
    print("=" * 60)

    if not os.path.exists(TABLES):
        print(f"\nERROR: Tables directory not found: {TABLES}")
        print("Run this script from the repo root directory.")
        sys.exit(1)

    print(f"\nBase: {BASE}")
    print(f"Tables: {TABLES}\n")

    print("--- Patching table calculated columns ---")
    for table in CALC_COLS:
        patch_table(table)

    print("\n--- Creating _Measures table ---")
    create_measures()

    print("\n--- Patching model.tmdl ---")
    patch_model()

    print("\n" + "=" * 60)
    print("Done! Close and reopen the .pbip in Power BI Desktop.")
    print("=" * 60)


if __name__ == '__main__':
    main()
