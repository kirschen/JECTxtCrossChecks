# Simple JEC txt-file cross-checks

Standalone script for performing simple cross-checks on JEC txt-files (warnings only useful for L2Relative files for now)

## Usage


```
cmsenv # in some CMSSW-environment to have JEC-related stuff available in script
python -b plotJECForEtaScanCleaned.py 

```
Dumps out root/pdf/png with canvas showing correction factors for a fine eta/pt-scan of the txt-files. Good for visual inspection. Also gives text-output to flag [obviously] problematic regions:
* Correction factors below 0.5/above 2 (for |eta|<2.5); below 0.3/above 3 (for |eta|>2.5)
* Correction factors changing rapidly (for 30% increase of pt changing by more than 30%)
* ... should become more clever