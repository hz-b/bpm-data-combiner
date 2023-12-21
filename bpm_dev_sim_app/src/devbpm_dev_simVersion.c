/* devbpm_dev_simVersion.c */
/* Example device support for the lsi (long string input) record
 * providing the module version string as the value
 */

#include <stddef.h>
#include <stdio.h>
#include <string.h>

#include "devSup.h"
#include "lsiRecord.h"

#include "bpm_dev_simVersion.h"

/* must be last include */
#include "epicsExport.h"

const char version[] = bpm_dev_simVERSION;

static long read_string(lsiRecord *prec)
{
    size_t N = sizeof version;
    char *buf = prec->val;

    if (N > prec->sizv)
        N = prec->sizv;
    prec->len = N;

    memcpy(buf, version, N);
    buf[N - 1] = '\0';

    return 0;
}

static lsidset devbpm_dev_simVersion = {
	{5, NULL, NULL, NULL, NULL}, read_string
};
epicsExportAddress(dset,devbpm_dev_simVersion);
