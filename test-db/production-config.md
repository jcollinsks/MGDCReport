# Production MGDC Connection Configuration

Restore these blocks when switching back to the real Analysis Services data source at work.

## expressions.tmdl

Replace the full expression block:

```tmdl
expression 'DirectQuery to AS - MGDC' =
	let
		Source = AnalysisServices.Database("powerbi://api.powerbi.com/v1.0/myorg/workforce", "MGDC"),
		Cubes = Table.Combine(Source[Data]),
		Cube = Cubes{[Id="Model", Kind="Cube"]}[Data]
	in
		Cube
	lineageTag: e1a00001-0001-0001-0001-000000000001

	annotation PBI_IncludeFutureArtifacts = True
```

## Table Partitions

Replace each table's partition block (at the bottom of each `.tmdl` file):

### SPOSites.tmdl

```tmdl
	partition SPOSites = entity
		mode: directQuery
		source
			entityName: SPOSites
			expressionSource: 'DirectQuery to AS - MGDC'
```

### SPOFiles.tmdl

```tmdl
	partition SPOFiles = entity
		mode: directQuery
		source
			entityName: SPOFiles
			expressionSource: 'DirectQuery to AS - MGDC'
```

### SPOFileActions.tmdl

```tmdl
	partition SPOFileActions = entity
		mode: directQuery
		source
			entityName: SPOFileActions
			expressionSource: 'DirectQuery to AS - MGDC'
```

### SPOPermissions.tmdl

```tmdl
	partition SPOPermissions = entity
		mode: directQuery
		source
			entityName: SPOPermissions
			expressionSource: 'DirectQuery to AS - MGDC'
```

### SPOGroups.tmdl

```tmdl
	partition SPOGroups = entity
		mode: directQuery
		source
			entityName: SPOGroups
			expressionSource: 'DirectQuery to AS - MGDC'
```

## Steps to Restore

1. Replace `expressions.tmdl` content with the expression block above
2. In each of the 5 table `.tmdl` files, replace the `partition` block at the bottom with the corresponding block above
3. Save all files and refresh the model in Power BI Desktop
