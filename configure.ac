#                                               -*- Autoconf -*-
# Process this file with autoconf to produce a configure script.

AC_PREREQ(2.52)

m4_define([required_lttoolbox_version], [3.3.1])
m4_define([required_apertium_version], [3.4.0])
m4_define([required_libxml_version], [2.6.17])
m4_define([required_libpcre_version], [6.4])

AC_INIT([ruLearn], [1.0.0], [vmsanchez@dlsi.ua.es])

AC_CONFIG_HEADERS([phrase-extraction/src/configure.H])

# Release versioning
GENERIC_MAJOR_VERSION=1
GENERIC_MINOR_VERSION=0
GENERIC_MICRO_VERSION=0

GENERIC_API_VERSION=$GENERIC_MAJOR_VERSION.$GENERIC_MINOR_VERSION
AC_SUBST(GENERIC_API_VERSION)

PACKAGE=ruLearn

GENERIC_VERSION=$GENERIC_MAJOR_VERSION.$GENERIC_MINOR_VERSION.$GENERIC_MICRO_VERSION
GENERIC_RELEASE=$GENERIC_MAJOR_VERSION.$GENERIC_MINOR_VERSION
AC_SUBST(GENERIC_RELEASE)
AC_SUBST(GENERIC_VERSION)

VERSION=$GENERIC_VERSION

AM_INIT_AUTOMAKE($PACKAGE, $VERSION, no-define)

# Checks for programs.

CXXFLAGS="-g"

AC_MSG_CHECKING([Compilation architecture: PPC, i686, Other])
ARCH=$(/bin/uname -m)
if test x$ARCH = xppc
then
  AC_MSG_RESULT([PowerPC])
  CFLAGS="$CFLAGS -std=c++11 -mpowerpc -maltivec -fno-pic -fomit-frame-pointer -Wall"
  CXXFLAGS="$CXXFLAGS -std=c++11 -mpowerpc -maltivec -fno-pic -fomit-frame-pointer -Wall"
else
  if test x$ARCH = xi686
  then
    AC_MSG_RESULT([i686])
    CFLAGS="$CFLAGS -std=c++11 -march=i686 -O3 -fno-pic -fomit-frame-pointer -Wall"
    CXXFLAGS="$CXXFLAGS -std=c++11 -march=i686 -O3 -fno-pic -fomit-frame-pointer -Wall"
  else
    AC_MSG_RESULT([Other])
    CFLAGS="$CFLAGS -std=c++11 -O3"
    CXXFLAGS="$CXXFLAGS -std=c++11 -O3"
  fi
fi

AC_PROG_CXX
#AC_PROG_LIBTOOL
AM_SANITY_CHECK
AC_LANG_CPLUSPLUS

AC_ARG_ENABLE(debug,
              [  --enable-debug    Enable "-g -Wall" compiler options],
              [CXXFLAGS="-g -Wall"; CFLAGS="-g -Wall"])

AC_ARG_ENABLE(profile,
              [  --enable-profile  Enable "-pg -g -Wall" compiler options],
              [CXXFLAGS="-pg -g -Wall"; CFLAGS="-pg -g -Wall"; LDFLAGS="-pg"])

#if test x$ARCH = xppc
#then
#  AC_PATH_PROG(XSLTPROC, sabcmd, no)
#  if test x$ac_cv_path_XSLTPROC = x
#  then
#    AC_MSG_ERROR([You don't have sablotron installed.])
#  fi
#  if test x$ac_cv_path_XSLTPROC = xno
#  then
#    AC_MSG_ERROR([You don't have sablotron installed.])
#  fi
#else
#  AC_PATH_PROG(XSLTPROC, xsltproc, no)
#  if test x$ac_cv_path_XSLTPROC = x
#  then
#    AC_MSG_ERROR([You don't have xsltproc installed.])
#  fi
#  if test x$ac_cv_path_XSLTPROC = xno
#  then
#    AC_MSG_ERROR([You don't have xsltproc installed.])
#  fi
#fi

AC_PATH_PROG(BASH, bash, no)
if test x$ac_cv_path_BASH = x
then
  AC_MSG_ERROR([You don't have bash installed.])
fi
if test x$ac_cv_path_BASH = xno
then
  AC_MSG_ERROR([You don't have bash installed.])
fi

AC_PATH_PROG(PERL, perl, no)
if test x$ac_cv_path_PERL = x
then
  AC_MSG_ERROR([You don't have perl installed.])
fi
if test x$ac_cv_path_PERL = xno
then
  AC_MSG_ERROR([You don't have perl installed.])
fi

AC_PATH_PROG(JAVA, java, no)
if test x$ac_cv_path_JAVA = x
then
  AC_MSG_ERROR([You don't have java installed.])
fi
if test x$ac_cv_path_JAVA = xno
then
  AC_MSG_ERROR([You don't have java installed.])
fi


#AC_PATH_PROG(APERTIUM_DESTXT, apertium-destxt, no)


AC_PATH_PROG(AWK, gawk, no)
if test x$ac_cv_path_AWK = x
then
  AC_MSG_ERROR([You don't have gawk installed.])
fi
if test x$ac_cv_path_AWK = xno
then
  AC_MSG_ERROR([You don't have gawk installed.])
fi

AC_PATH_PROG(PKG_CONFIG, pkg-config, no)
if test x$ac_cv_path_PKG_CONFIG = x
then
  AC_MSG_ERROR([You don't have pkg-config installed.])
fi
if test x$ac_cv_path_PKG_CONFIG = xno
then
  AC_MSG_ERROR([You don't have pkg-config installed.])
fi


# Checking zlib
echo Checking zlib
AC_CHECK_HEADERS(zlib.h,
  AC_CHECK_LIB(z, gzread,[
    AC_DEFINE([HAVE_LIBZ], [], [Have compression library])
      if test "x${Z_DIR}" != "x"
      then
        Z_CFLAGS="-I${Z_DIR}/include"
        Z_LIBS="-L${Z_DIR}/lib -lz"
      else
        Z_LIBS="-lz"
      fi]))

AC_SUBST(Z_CFLAGS)
AC_SUBST(Z_LIBS)

AC_CHECK_HEADER(pcreposix.h,
  AC_CHECK_LIB(pcre, pcre_info,[
  LIBS="$LIBS -lpcreposix -lpcre"
  no_comp_check=yes],
  AC_MSG_ERROR([*** unable to locate pcre library ***])),
  AC_MSG_ERROR([*** unable to locate pcreposix.h include file ***]))

PKG_CHECK_MODULES(LIBXML2, [dnl
  libxml-2.0 >= required_libxml_version])

PKG_CHECK_MODULES(LTTOOLBOX, [dnl
  lttoolbox >= required_lttoolbox_version])

PKG_CHECK_MODULES(APERTIUM, [dnl
  apertium >= required_apertium_version])

#check whether Apertium is patched
AC_MSG_CHECKING([whether Apertium supports rule cancellation ])
  ac_supports_cancellation=`bash apertium-patch/test/testApertiumPatchAutoconf.sh "$APERTIUM_LIBS"`
  if test "$ac_supports_cancellation" = "True";
  then
    AC_MSG_RESULT([yes])
  else
    AC_MSG_RESULT([no])
    AC_MSG_ERROR([Your Apertium installation does not support rule cancellation. Please install latest version from SVN or use the provided patch in apertium-patch directory
])
  fi


AC_PATH_PROG(XMLLINT, xmllint, no)

#Check for libraries.
AC_CHECK_LIB(xml2, xmlReaderForFile)

# Checks for header files.
AC_HEADER_STDC
AC_CHECK_HEADERS([regex.h sys/types.h sys/times.h sys/wait.h sys/resource.h locale.h getopt.h])

# Checks for typedefs, structures, and compiler characteristics.
AC_HEADER_STDBOOL
AC_C_CONST
AC_TYPE_SIZE_T

# Checks for library functions.
AC_FUNC_ERROR_AT_LINE
AC_FUNC_MALLOC
AC_FUNC_REALLOC

#AC_CHECK_DECLS([fread_unlocked, fwrite_unlocked, fgetc_unlocked, fputc_unlocked, fputs_unlocked, getopt_long])
AC_CHECK_DECLS([getopt_long])

#AC_CHECK_FUNCS([setlocale strdup])
#AC_CHECK_FUNCS([setlocale])


AC_CHECK_PROG(PARALLEL, parallel,yes)
if test x"$PARALLEL" != x"yes" ; then
    AC_MSG_ERROR([Please install the parallel command from the moreutils package: http://joeyh.name/code/moreutils/.])
fi
AC_MSG_CHECKING([for the right version of parallel])
  ac_supports_parallel_ver=`parallel --version 2>/dev/null | grep 'GNU Parallel'`
  if test "$ac_supports_parallel_ver" = "";
  then
    AC_MSG_RESULT([yes])
  else
    AC_MSG_RESULT([no])
    AC_MSG_ERROR([It seems that you have GNU parallel installed in your system. Please replace it with Coreutils parallel: http://joeyh.name/code/moreutils/
])
fi


AM_PATH_PYTHON([2.6.7], , [AC_MSG_ERROR([You do not have Python 2.6.7 or later installed.])])
  AC_MSG_CHECKING([for PuLP for Python])
  ac_supports_python_ver=`$PYTHON -c "import sys; \
import pulp; \
var = True; \
print (var)" 2> /dev/null`
  if test "$ac_supports_python_ver" = "True";
  then
    AC_MSG_RESULT([yes])
  else
    AC_MSG_RESULT([no])
    AC_MSG_ERROR([this package requires the PuLP library for Python. Please, install it and try again: http://pythonhosted.org/PuLP/main/installing_pulp_at_home.html
])
  fi
  AC_MSG_CHECKING([for argparse for Python])
  ac_supports_python_ver=`$PYTHON -c "import sys; \
import argparse; \
var = True; \
print (var)" 2> /dev/null`
  if test "$ac_supports_python_ver" = "True";
  then
    AC_MSG_RESULT([yes])
  else
    AC_MSG_RESULT([no])
    AC_MSG_ERROR([this package requires the argparse module for Python. Please, install it and try again.
])
  fi



AC_OUTPUT([Makefile phrase-extraction/Makefile phrase-extraction/src/Makefile rule-generalisation/Makefile giza-pp/GIZA++-v2/Makefile giza-pp/mkcls-v2/Makefile  ruLearn-1.0.pc])
