-- ============================================================
-- MGDC Test Database — Table Definitions
-- Matches Analysis Services entity schemas exactly
-- Column names with dots use [bracket] quoting
-- ============================================================

-- Drop tables if they exist (for re-runs)
IF OBJECT_ID('dbo.SPOGroups', 'U') IS NOT NULL DROP TABLE dbo.SPOGroups;
IF OBJECT_ID('dbo.SPOPermissions', 'U') IS NOT NULL DROP TABLE dbo.SPOPermissions;
IF OBJECT_ID('dbo.SPOFileActions', 'U') IS NOT NULL DROP TABLE dbo.SPOFileActions;
IF OBJECT_ID('dbo.SPOFiles', 'U') IS NOT NULL DROP TABLE dbo.SPOFiles;
IF OBJECT_ID('dbo.SPOSites', 'U') IS NOT NULL DROP TABLE dbo.SPOSites;
GO

-- ============================================================
-- 1. SPOSites — 25 source columns
-- ============================================================
CREATE TABLE dbo.SPOSites (
    Id                              NVARCHAR(100)   NOT NULL,
    Url                             NVARCHAR(500)   NOT NULL,
    [RootWeb.Title]                 NVARCHAR(255)   NULL,
    [RootWeb.WebTemplate]           NVARCHAR(50)    NULL,
    CreatedTime                     DATETIME2       NULL,
    LastContentChange               DATETIME2       NULL,
    StorageUsed                     BIGINT          NULL,
    StorageQuota                    BIGINT          NULL,
    IsInRecycleBin                  BIT             NULL,
    [SensitivityLabelInfo.Id]       NVARCHAR(100)   NULL,
    [SensitivityLabelInfo.DisplayName] NVARCHAR(100) NULL,
    IsExternalSharingEnabled        BIT             NULL,
    [Owner.Email]                   NVARCHAR(320)   NULL,
    [Owner.Name]                    NVARCHAR(255)   NULL,
    GroupId                         NVARCHAR(100)   NULL,
    IsTeamsConnectedSite            BIT             NULL,
    ReadLocked                      BIT             NULL,
    HubSiteId                       NVARCHAR(100)   NULL,
    BlockAccessFromUnmanagedDevices BIT             NULL,
    GeoLocation                     NVARCHAR(10)    NULL,
    SnapshotDate                    DATETIME2       NULL,
    LastSecurityModifiedDate        DATETIME2       NULL,
    IsCommunicationSite             BIT             NULL,
    IsOneDrive                      BIT             NULL,
    Privacy                         NVARCHAR(20)    NULL,
    CONSTRAINT PK_SPOSites PRIMARY KEY (Id)
);
GO

-- ============================================================
-- 2. SPOFiles — 22 source columns
-- ============================================================
CREATE TABLE dbo.SPOFiles (
    SiteId                          NVARCHAR(100)   NOT NULL,
    ItemId                          NVARCHAR(100)   NOT NULL,
    FileName                        NVARCHAR(500)   NULL,
    Extension                       NVARCHAR(20)    NULL,
    SizeInBytes                     BIGINT          NULL,
    SizeInBytesWithVersions         BIGINT          NULL,
    TimeCreated                     DATETIME2       NULL,
    TimeLastModified                DATETIME2       NULL,
    [Author.Email]                  NVARCHAR(320)   NULL,
    [Author.Name]                   NVARCHAR(255)   NULL,
    [ModifiedBy.Email]              NVARCHAR(320)   NULL,
    [ModifiedBy.Name]               NVARCHAR(255)   NULL,
    [SensitivityLabelInfo.Id]       NVARCHAR(100)   NULL,
    [SensitivityLabelInfo.DisplayName] NVARCHAR(100) NULL,
    IsLabelEncrypted                BIT             NULL,
    MajorVersion                    BIGINT          NULL,
    MinorVersion                    BIGINT          NULL,
    DirName                         NVARCHAR(500)   NULL,
    SiteUrl                         NVARCHAR(500)   NULL,
    WebId                           NVARCHAR(100)   NULL,
    ListId                          NVARCHAR(100)   NULL,
    SnapshotDate                    DATETIME2       NULL,
    CONSTRAINT PK_SPOFiles PRIMARY KEY (SiteId, ItemId)
);
GO

-- ============================================================
-- 3. SPOFileActions — 17 source columns
-- ============================================================
CREATE TABLE dbo.SPOFileActions (
    SiteId                          NVARCHAR(100)   NOT NULL,
    SiteUrl                         NVARCHAR(500)   NULL,
    WebId                           NVARCHAR(100)   NULL,
    ListId                          NVARCHAR(100)   NULL,
    ListItemId                      NVARCHAR(100)   NOT NULL,
    ItemURL                         NVARCHAR(500)   NULL,
    ItemName                        NVARCHAR(500)   NULL,
    ItemExtension                   NVARCHAR(20)    NULL,
    ActionDate                      DATETIME2       NOT NULL,
    ActorType                       NVARCHAR(50)    NULL,
    ActorIdType                     NVARCHAR(50)    NULL,
    ActorDisplayName                NVARCHAR(255)   NULL,
    ActorEmail                      NVARCHAR(320)   NULL,
    ActionName                      NVARCHAR(100)   NOT NULL,
    UserAgent                       NVARCHAR(500)   NULL,
    ClientIP                        NVARCHAR(50)    NULL,
    SnapshotDate                    DATETIME2       NULL
);
GO

-- ============================================================
-- 4. SPOPermissions — 21 source columns
-- ============================================================
CREATE TABLE dbo.SPOPermissions (
    SiteId                          NVARCHAR(100)   NOT NULL,
    WebId                           NVARCHAR(100)   NULL,
    ListId                          NVARCHAR(100)   NULL,
    ListItemId                      NVARCHAR(100)   NULL,
    UniqueId                        NVARCHAR(100)   NOT NULL,
    ItemType                        NVARCHAR(50)    NULL,
    ItemURL                         NVARCHAR(500)   NULL,
    FileExtension                   NVARCHAR(20)    NULL,
    RoleDefinition                  NVARCHAR(50)    NULL,
    LinkId                          NVARCHAR(100)   NULL,
    ScopeId                         NVARCHAR(100)   NULL,
    LinkScope                       NVARCHAR(50)    NULL,
    TotalUserCount                  BIGINT          NULL,
    [ShareCreatedBy.Email]          NVARCHAR(320)   NULL,
    [ShareCreatedBy.Name]           NVARCHAR(255)   NULL,
    ShareCreatedTime                DATETIME2       NULL,
    [ShareLastModifiedBy.Email]     NVARCHAR(320)   NULL,
    [ShareLastModifiedBy.Name]      NVARCHAR(255)   NULL,
    ShareLastModifiedTime           DATETIME2       NULL,
    ShareExpirationTime             DATETIME2       NULL,
    SnapshotDate                    DATETIME2       NULL,
    CONSTRAINT PK_SPOPermissions PRIMARY KEY (UniqueId)
);
GO

-- ============================================================
-- 5. SPOGroups — 9 source columns
-- ============================================================
CREATE TABLE dbo.SPOGroups (
    SiteId                          NVARCHAR(100)   NOT NULL,
    GroupId                         BIGINT          NOT NULL,
    GroupLinkId                     NVARCHAR(100)   NULL,
    GroupType                       NVARCHAR(50)    NULL,
    DisplayName                     NVARCHAR(255)   NULL,
    [Owner.Email]                   NVARCHAR(320)   NULL,
    [Owner.Name]                    NVARCHAR(255)   NULL,
    [Owner.Type]                    NVARCHAR(50)    NULL,
    SnapshotDate                    DATETIME2       NULL,
    CONSTRAINT PK_SPOGroups PRIMARY KEY (SiteId, GroupId)
);
GO

PRINT 'All 5 MGDC tables created successfully.';
GO
