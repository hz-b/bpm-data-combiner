#include <aSubRecord.h>
#include <menuFtype.h>
#include <registryFunction.h>
#include <epicsExport.h>
#include <algorithm>
#include <cstring>
#include <cstdio>

/*
 * forward as single array from one location to the next
 */
extern "C" {
    static long array_forward(aSubRecord *prec);
}

static int element_length_from(const int ftype, const int verbose, const char* recordname, const char * field){
    switch(ftype){

    case menuFtypeCHAR  : return sizeof( epicsInt8   ); break;
    case menuFtypeUCHAR : return sizeof( epicsUInt8  ); break;
    case menuFtypeSHORT : return sizeof( epicsInt16  ); break;
    case menuFtypeUSHORT: return sizeof( epicsUInt16 ); break;
    case menuFtypeLONG  : return sizeof( epicsInt32  ); break;
    case menuFtypeULONG : return sizeof( epicsUInt32 ); break;
      /*
	only epics 7
    case menuFtypeINT64 : return sizeof( epicsInt64  ); break;
    case menuFtypeUINT64: return sizeof( epicsUInt64 ); break;
      */
	// case menuFtypeFLOAT : return sizeof( epicsFloat  ); break;
	// case menuFtypeDOUBLE: return sizeof( epicsDouble ); break;

    default:
	if(verbose){
	    printf("%s:%s could not resolve ftype %d\n", recordname, field, ftype);
	}
	return -1;
    }

    if(verbose){
	printf("%s:%s should not end up here!\n", recordname, field);
    }
    return -1;
}

long array_forward(aSubRecord *prec)
{
    const int verbose = (prec->tpro) ? 1 : 0;
    if(verbose){
	printf("Record %s: trace processing %d\n", prec->name, prec->tpro);
    }

    /* check that input array exists */
    if(prec->a == NULL){
	assert(0);
	return -1;
    }
    /* check that output array exists */
    if(prec->vala == NULL){
	assert(0);
	return -1;
    }

    if(prec->ftva != prec->fta){
	if(verbose){
	    printf("%s.%s: output array %s.vala is of type %d that does not match input type of array a %d\n",
		   __FILE__, __FUNCTION__, prec->name, (int) prec->ftva, (int) prec->fta);
	}
	return -1;
    }

    epicsUInt32 nea = std::min(prec->nea, prec->nova);
    if(prec->nea != nea){
	if(verbose){
	    printf("%s.%s: input array %s.a uses %u elements but output vala provides only %u, thus only copying %u\n",
		   __FILE__, __FUNCTION__, prec->name, prec->nea, prec->nova, nea);
	}
    }

    static int elem_size_in = element_length_from(prec->fta, verbose, prec->name, "A");
    if (elem_size_in <= 0){
	if(verbose){
	    printf("%s.%s: inp/out array %s.a/vala fta %d size could not be found\n",
		   __FILE__, __FUNCTION__, prec->name, prec->fta);
	}
	return -1;
    }

    // now all good?
    prec->neva = nea;
    memcpy(prec->vala, prec->a, elem_size_in * nea);
    if(verbose){
	printf("%s.%s: record %s copied a->vala\n",
	       __FILE__, __FUNCTION__, prec->name);
    }
    return 0;

}
epicsRegisterFunction(array_forward);
