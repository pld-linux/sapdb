
# TODO:
#	- Correct web server pages to work fine with konqueror.
#	- Creating databases via web interfaces do not work fine yet.
#	- All scripts which use dbmcli look for an exit result grepping
#         dbmcli output and searching "OK" phrase. It's wrong while error
#	  messages can contains "OK" phrase too.
#	- A sweet dream: dynamic linking...

%define		mainver		7.4
%define		subver		3.17
%define		intversion	V74_03_17

Summary:	SAP DB
Name:		sapdb
Version:	%{mainver}.%{subver}
Release:	0.5
License:	GPL
Group:		Applications/Databases
Source0:	ftp://ftp.sap.com/pub/sapdb/%{mainver}/sapdb-source-%{mainver}.0%{subver}.tgz
Source1:	ftp://ftp.sap.com/pub/sapdb/%{mainver}/sapdb-devtools-src.tgz
Source2:	ftp://ftp.sap.com/pub/sapdb/%{mainver}/sapdb-htmldoc-%{mainver}.tgz
Source3:	%{name}.init
Source4:	%{name}-web.init
Source5:	%{name}-suse-demo.tar.bz2
Source6:	%{name}-sysconfig
Source7:	%{name}-suse-README
Source8:	%{name}-suse-pam
Source10:	migration73_74eng.pdf
Source11:	%{name}-suse-rpm.lst
Source12:	%{name}-suse-firststeps.tgz
Patch0:		%{name}-suse-desc.patch
Patch2:		%{name}-suse-src.patch
Patch4:		%{name}-suse-python22.patch
Patch5:		%{name}-suse-perl.patch
Patch6:		%{name}-suse-permissions.patch
Patch7:		%{name}-suse-fhs.patch
Patch8:		%{name}-suse-readline.patch
Patch9:		%{name}-suse-pam.patch
Patch10:	%{name}-suse-devtools.patch
Patch11:	%{name}-suse-devtools-lcmake.patch
Patch12:	%{name}-suse-devtools-makedepend.patch
Patch13:	%{name}-suse-devtools-gcc33.patch
Patch14:	%{name}-suse-devtools-alltools.patch
Patch15:	%{name}-suse-gcc33-workaround.patch
Patch16:	%{name}-suse-instlserver.patch
Patch17:	%{name}-suse-wahttp-pidfile.patch
Patch18:	%{name}-suse-optimize-gcc33.patch
Patch19:	%{name}-bash.patch
Patch20:	%{name}-desc.patch
Patch21:	%{name}-webpages.patch
BuildRequires:	bash
BuildRequires:	ncurses-static
BuildRequires:	bison
BuildRequires:	perl
BuildRequires:	python >= 2.2
BuildRequires:	python-libs >= 2.2
BuildRequires:	python-devel >= 2.2
BuildRequires:	libsigc++-static >= 1.2.4
BuildRequires:	glibc-devel
BuildRequires:	pam-devel
URL:		http://www.sapdb.org/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		sapdbdir	%{_libdir}/%{name}
%define		sapdbvar	/var/lib/%{name}
%define		sqlspool	/var/spool/sql

%define		_noautocompressdoc *.doc

%description
SAP DB


%package docs
Summary:	SAP DB documentation
Group:		Applications/Databases

%description docs
HTML documentation for SAP DB.
For more information please see www.sapdb.org.


%package ind
Summary:	SAP DB - release independend programs
Group:		Applications/Databases
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires(postun):	/usr/sbin/userdel
Requires(postun):	/usr/sbin/groupdel
Requires(post,postun):	/sbin/chkconfig
Requires:	python >= 2.2
Requires:	python-modules >= 2.2

%description ind 
- remote communication server
- command line tools for database administration
- precompiler runtime (for applications built by SAP DB precompiler)
For more information please see www.sapdb.org.


%package srv
Summary:	SAP DB Database Server
Group:		Applications/Databases
Requires(pre):	%{name}-ind = %{version}
Requires(post,postun):	/sbin/chkconfig

%description srv
SAP DB Database Server


%package web
Summary:      SAP DB Web Tools
Group:        Applications/Databases
Requires:     sapdb-callif >= %{version}

%description web
SAP DB Web Tools


%package precompiler
Summary:      SAP DB Precompiler
Group:        Applications/Databases
PreReq:       sapdb-ind >= %{version}

%description precompiler
SAP DB Precompiler


%package callif
Summary:      SAP DB ODBC and JDBC Interfaces
Group:        Applications/Databases

%description callif
- ODBC driver
- JDBC driver
For more information please see www.sapdb.org.


%package scriptif
Summary:      SAP DB Perl and Python Interfaces
Group:        Applications/Databases
PreReq:       sapdb-ind >= %{version}

%description scriptif
SAP DB Perl and Python Interfaces


%package testdb
Summary:      SAP DB test database
Group:        Applications/Databases
PreReq:       sapdb-ind sapdb-srv

%description testdb
This package contains a script tp create and immediately start
a database instance TST(having 20 MB Data space and 8 MB log space). 
Please remember to shutdown database before system shutdown. 
- sample database user: TEST, password TEST
- DBM user: DBM, password DBM
- database administrator: DBA, password DBA 
A script to remove this database is also included.
The scripts can be found in the %{sapdbdir}/testdb directory, and should be
started as user sapdb.


%prep
%setup -q -c -a0 -T
mkdir -p $RPM_BUILD_DIR/%{name}-%{version}/buildtools
tar xzf %{SOURCE1} -C $RPM_BUILD_DIR/%{name}-%{version}/buildtools
tar xzf %{SOURCE2} -C $RPM_BUILD_DIR/%{name}-%{version}
mv $RPM_BUILD_DIR/%{name}-%{version}/htmldoc-74 $RPM_BUILD_DIR/%{name}-%{version}/html
tar xzf %{SOURCE12} -C $RPM_BUILD_DIR/%{name}-%{version}/html
bzip2 -dc %{SOURCE5} | tar xf - -C $RPM_BUILD_DIR/%{name}-%{version}

cd $RPM_BUILD_DIR/%{name}-%{version}/%{intversion}
%patch0
%patch2
%patch4
%patch5
%patch6
%patch7
%patch8
%patch9
%patch15
%patch16
%patch17
%patch20 -p1
%patch21 -p1

cd $RPM_BUILD_DIR/%{name}-%{version}/buildtools
%patch10 -p1
%patch11
%patch12 -p1
%patch13
%patch14
%patch18
%patch19 -p1

%build
# generate sapdb build tools
chmod -R u+w $RPM_BUILD_DIR/%{name}-%{version}/buildtools
cd $RPM_BUILD_DIR/%{name}-%{version}/buildtools
NOREG=1
export NOREG
#export USE_AUTOCONF=yes
%configure
%{__make}

cd $RPM_BUILD_DIR/%{name}-%{version}

$RPM_BUILD_DIR/%{name}-%{version}/buildtools/bin/newSapdbSrc.py \
    $RPM_BUILD_DIR/%{name}-%{version}/%{intversion}/SAPDB_ORG

IPROF=$RPM_BUILD_DIR/%{name}-%{version}/%{intversion}/SAPDB_ORG/.iprofile
cp $IPROF $IPROF.tmp
cat $IPROF.tmp | egrep -v "PYTHON_INCLUDE|PYTHON_LIBDIR|NOQUIET|NOREG" > $IPROF
echo "PYTHON_LIBDIR=/usr/lib/python2.2 export PYTHON_LIBDIR" >> $IPROF
echo "PYTHON_INCLUDE=/usr/include/python2.2 export PYTHON_INCLUDE" >> $IPROF
echo "NOQUIET=1 export NOQUIET" >> $IPROF
echo "NOREG=1 export NOREG" >> $IPROF

. $RPM_BUILD_DIR/%{name}-%{version}/%{intversion}/SAPDB_ORG/.iprofile

imf -x all ||:
# workaround for wrong build order - check for better solution
imf -x all ||:
imf -x all 

#ims -eU kernel
%ifarch %{ix86} ia64 x86_64
ims -x slowknl
%endif

%install
rm -rf $RPM_BUILD_ROOT

#
# Prepare environment for packaging
#
ORG=$RPM_BUILD_DIR/%{name}-%{version}/%{intversion}/SAPDB_ORG

mkdir -p \
    $RPM_BUILD_ROOT/etc/sysconfig \
    $RPM_BUILD_ROOT%{sapdbdir}/depend/wrk \
    $RPM_BUILD_ROOT%{sapdbdir}/testdb \
    $RPM_BUILD_ROOT%{sqlspool}/ini \
    $RPM_BUILD_ROOT%{sqlspool}/dbspeed \
    $RPM_BUILD_ROOT%{sqlspool}/diag \
    $RPM_BUILD_ROOT%{sqlspool}/fifo \
    $RPM_BUILD_ROOT%{sqlspool}/ipc \
    $RPM_BUILD_ROOT%{sqlspool}/pid \
    $RPM_BUILD_ROOT%{sqlspool}/ppid \
    $RPM_BUILD_ROOT%{sapdbvar}/indep_data/config \
    $RPM_BUILD_ROOT%{sapdbvar}/indep_data/wrk \
    $RPM_BUILD_ROOT%{_libdir}/python2.2

sed 's:$OWN32:%{sapdbdir}/web:g 
s:$OWN64:%{sapdbdir}/web:g
s:$LOG:/var/log/sapdb:g
s:Port=85:Port=9999:g' $ORG/usr/config/WebAgent74.ini \
    > $RPM_BUILD_ROOT%{sqlspool}/ini/WebAgent74.ini

#
# install DEMO scripts
#
for i in $RPM_BUILD_DIR/%{name}-%{version}/demo/*; do
    rm -f $RPM_BUILD_ROOT%{sapdbdir}/testdb/`basename $i`
    sed 's:/opt/sapdb:%{sapdbdir}:g
s:/bin/sh:/bin/bash:' $i \
    > $RPM_BUILD_ROOT%{sapdbdir}/testdb/`basename $i`
done

#
# install SAPDB files
#
awk -F\; '!/^#/ {print $1 " " $2}' %SOURCE11 | while read a b
do
   if [ -f $ORG/usr/$a ]; then
       mkdir -p `dirname $RPM_BUILD_ROOT%{sapdbdir}/$b`
       cp -p $ORG/usr/$a $RPM_BUILD_ROOT%{sapdbdir}/$b
   fi
done

#
# init stuff
#
mkdir -p $RPM_BUILD_ROOT/var/adm/fillup-templates \
         $RPM_BUILD_ROOT/etc/rc.d/init.d \
         $RPM_BUILD_ROOT/var/log/sapdb \
         $RPM_BUILD_ROOT/var/run/wahttp
install -m 600 %{SOURCE6} $RPM_BUILD_ROOT/etc/sysconfig/sapdb
install -m 744 %{SOURCE3} $RPM_BUILD_ROOT/etc/rc.d/init.d/sapdb
install -m 754 %{SOURCE4} $RPM_BUILD_ROOT/etc/rc.d/init.d/sapdb-web

#
# PAM
#
mkdir -p $RPM_BUILD_ROOT/etc/pam.d
install -m 644 %{SOURCE8} $RPM_BUILD_ROOT/etc/pam.d/sapdb

#
# Documentation
#
cp %{SOURCE7}	$RPM_BUILD_DIR/%{name}-%{version}/README.SuSE 
cp %{SOURCE10}	$RPM_BUILD_DIR/%{name}-%{version}

#
# use PLD Python
#
mv $RPM_BUILD_ROOT%{sapdbdir}/depend/lib/python1.5/* \
    $RPM_BUILD_ROOT%{_libdir}/python2.2
rmdir $RPM_BUILD_ROOT%{sapdbdir}/depend/lib/python1.5
ln -sf %{_libdir}/python2.2 $RPM_BUILD_ROOT%{sapdbdir}/depend/lib/python1.5
ln -sf /usr/bin/python $RPM_BUILD_ROOT%{sapdbdir}/depend/pgm/python

#
# sapdb user HOME scripts
#
cat <<EOF > $RPM_BUILD_ROOT%{sapdbvar}/.profile
INDEP=%{sapdbdir}/indep_prog
DEP=%{sapdbdir}/depend

SAPDBROOT=$DEP
PATH=$PATH:$IND/bin:$DEP/bin
#CLASSPATH=$CLASSPATH:$SAPDBROOT/misc/sapdbc.jar:.
#PERL5LIB=$PERL5LIB:$SAPDBROOT/misc
#PYTHONPATH=$PYTHONPATH:$SAPDBROOT/misc

export INDEP DEP SAPDBROOT PATH 
#export PYTHONPATH
#export CLASSPATH
#export PERL5LIB
EOF


%clean
rm -rf $RPM_BUILD_ROOT

%pre ind
if [ -z "`getgid %{name}`" ]; then
	/usr/sbin/groupadd -g 101 -r %{name} 2> /dev/null || true
fi

if [ -z "`id -u %{name} 2>/dev/null`" ]; then
	/usr/sbin/useradd -u 101 -g %{name} -M -r -d %{sapdbvar} -s /bin/bash \
		-c "SAP DB" %{name} 2> /dev/null || true
fi

%post ind
if [ "$1" = "2" ]; then
    # update
    FILE=%{sqlspool}/ini/SAP_DBTech.ini
    if [ -f $FILE ]; then
	i=0
	while [ -f $FILE.$i ]; do let i++; done
	echo "- saving $FILE as $FILE.$i"
	cp $FILE $FILE.$i
	[ $? -ne 0 ] && exit 1
    else
	echo "update error: file $FILE not found!" >&2
	exit 1
    fi
fi

DBROOT=%{sapdbdir}/indep_prog
export DBROOT

o=`$DBROOT/bin/dbmcli -s dbm_setpath IndepDataPath %{sapdbvar}/indep_data`
t=`echo $o | grep OK`
if [ "$t" = "" ]; then
    echo "- could not set inpedendent data path: $o" >&2
    exit 1
fi

o=`$DBROOT/bin/dbmcli -s dbm_setpath IndepProgPath %{sapdbdir}/indep_prog`
t=`echo $o | grep OK`
if [ "$t" = "" ]; then
    echo "- could not set independent program path: $o" >&2
    exit 1
fi

#register precompiler runtime
%{sapdbdir}/indep_prog/bin/irconf -i -p %{sapdbdir}/indep_prog/runtime/7403 >/dev/null 2>&1 || :
%{sapdbdir}/indep_prog/bin/irconf -i -p %{sapdbdir}/indep_prog/runtime/7300 >/dev/null 2>&1 || :
%{sapdbdir}/indep_prog/bin/irconf -i -p %{sapdbdir}/indep_prog/runtime/7250 >/dev/null 2>&1 || :
%{sapdbdir}/indep_prog/bin/irconf -i -p %{sapdbdir}/indep_prog/runtime/7240 >/dev/null 2>&1 || :
exit 0	

%preun ind
%{sapdbdir}/indep_prog/bin/irconf -r -p %{sapdbdir}/indep_prog/runtime/7403 >/dev/null 2>&1 || :
%{sapdbdir}/indep_prog/bin/irconf -r -p %{sapdbdir}/indep_prog/runtime/7300 >/dev/null 2>&1 || :
%{sapdbdir}/indep_prog/bin/irconf -r -p %{sapdbdir}/indep_prog/runtime/7250 >/dev/null 2>&1 || :
%{sapdbdir}/indep_prog/bin/irconf -r -p %{sapdbdir}/indep_prog/runtime/7240 >/dev/null 2>&1 || :

if [ "$1" != "0" ]; then
    # do nothing in upgrade case
    exit 0
fi

DBROOT=%{sapdbdir}/indep_prog
export DBROOT

o=`fuser $DBROOT/bin/* $DBROOT/pgm/* 2>/dev/null`
if [ $? -eq 0 ]; then
    if [ `echo $o | wc -l` -eq 1 -a `echo $o | grep -c "^$DBROOT/pgm/vserver"` -eq 1 ]; then
        $DBROOT/bin/x_server stop >/dev/null 2>&1
    else
        echo "- aborting (software is in use)" >&2
        exit 1
    fi
fi

rm -rf %{sapdbvar}/indep_data/wrk/_OPTSAPD >/dev/null 2>&1
rm -f %{sapdbvar}/indep_data/wrk/dbmsrv.prt >/dev/null 2>&1
rm -f %{sapdbvar}/indep_data/config/_OPTSAPD* >/dev/null 2>&1
rm -f %{sapdbvar}/indep_data/wrk/vserver.prot >/dev/null 2>&1
rm -f %{sqlspool}/ini/SAP_DBTech.ini* > /dev/null 2>&1
rm -rf %{sapdbvar}/indep_data/wrk/irtrace* >/dev/null 2>&1
rm -f %{sapdbvar}/indep_data/config/Registry1.dcom >/dev/null 2>&1
rm -f %{sqlspool}/ini/Registry_dcom.ini >/dev/null 2>&1
rm -rf %{sapdbvar}/indep_data/wrk/root >/dev/null 2>&1
exit 0

%postun ind
if [ "$1" = "0" ] ; then
	/usr/sbin/userdel sapdb 2> /dev/null || true
	/usr/sbin/groupdel sapdb 2> /dev/null || true
fi

%post srv
/sbin/chkconfig --add sapdb
if [ -f /var/lock/subsys/sapdb ]; then
	/etc/rc.d/init.d/sapdb restart 1>&2
else
	echo "Run \"/etc/rc.d/init.d/sapdb start\" to start SAP DB."
fi

DBROOT=%{sapdbdir}/depend
export DBROOT

o=`su - sapdb -c "umask 0003; $DBROOT/bin/dbmcli -s -R $DBROOT inst_reg -k $DBROOT"`
t=`echo $o | grep OK`
if [ "$t" = "" ]; then
    echo "- could not register the installation: $o" >&2
    exit 1
fi

dcom_link=%{sapdbdir}/depend/wrk/Registry.dcom
if [ -e $dcom_link ] && [ ! -L $dcom_link ]; then
       rm $dcom_link >/dev/null 2>&1
fi

if test -x $DBROOT/lib/dbpinstall.so ; then
    o=`$DBROOT/bin/xregcomp -c $DBROOT/lib/dbpinstall 2>&1`
else
    o=`$DBROOT/bin/xregcomp -c $DBROOT/lib/lib64/dbpinstall 2>&1`
fi

t=`echo $o | grep "Registration done"`
if [ "$t" = "" ]; then
    echo "- could not register dbpinstall: $o" >&2
    exit 1
fi

exit 0

%preun srv
if [ "$1" != "0" ]; then
    # do nothing in upgrade case
    exit 0
fi

if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/sapdb ]; then
		/etc/rc.d/init.d/sapdb stop 1>&2
	fi
	/sbin/chkconfig --del sapdb
fi

DBROOT=%{sapdbdir}/depend
export DBROOT

IND_PROG_DBROOT=`$DBROOT/bin/dbmcli dbm_getpath IndepProgPath 2>&1 | awk 'BEGIN {ok=0} NR==1 && $1="OK" {ok=1} NR==2 && ok!=0 {print $0}'`
[ -z "$IND_PROG_DBROOT" -a -f %{sqlspool}/ini/SAP_DBTech.ini ] &&
IND_PROG_DBROOT=`grep '^IndepPrograms=' %{sqlspool}/ini/SAP_DBTech.ini | sed 's:IndepPrograms=::g'`
[ ! -z "$IND_PROG_DBROOT" ] && $IND_PROG_DBROOT/bin/x_server start >/dev/null 2>&1
IND_DATA_DBROOT=`$DBROOT/bin/dbmcli dbm_getpath IndepDataPath 2>&1 | awk 'BEGIN {ok=0} NR==1 && $1="OK" {ok=1} NR==2 && ok!=0 {print $0}'`
[ -z "$IND_DATA_DBROOT" -a -f %{sqlspool}/ini/SAP_DBTech.ini ] &&
IND_DATA_DBROOT=`grep '^IndepData=' %{sqlspool}/ini/SAP_DBTech.ini | sed 's:IndepData=::g'`
$DBROOT/bin/dbmcli -s -R $DBROOT inst_unreg $DBROOT >/dev/null 2>&1

o=`fuser $DBROOT/bin/* $DBROOT/pgm/* 2>/dev/null`
if [ $? -eq 0 ]; then
    if [ `echo $o | wc -l` -eq 1 -a `echo $o | grep -c "^$DBROOT/pgm/vserver"` -eq 1 ]; then
        $DBROOT/bin/x_server stop >/dev/null 2>&1
    else
        echo "- aborting (software is in use)" >&2
        exit 1
    fi
fi

rm -f $DBROOT/env/_OPTSAPD* $DBROOT/load.prot >/dev/null 2>&1
rm -f $DBROOT/wrk/Registry.dcom*  >/dev/null 2>&1
rm -f %{sapdbvar}/indep_data/config/Registry1.dcom >/dev/null 2>&1
rm -f %{sqlspool}/ini/Registry_dcom.ini >/dev/null 2>&1
rm -f %{sqlspool}/ini/odbc.ini >/dev/null 2>&1
if [ ! -z "$IND_DATA_DBROOT" ]; then
    rm -f \
        $IND_DATA_DBROOT/config/_OPTSAPD* \
        $IND_DATA_DBROOT/wrk/dbmsrv.prt \
        >/dev/null 2>&1
    rm -rf $IND_DATA_DBROOT/wrk/_OPTSAPD* >/dev/null 2>&1
fi
exit 0

%post web
/sbin/chkconfig --add sapdb-web
if [ -f /var/lock/subsys/sapdb-web ]; then
	/etc/rc.d/init.d/sapdb-web restart 1>&2
else
	echo "Run \"/etc/rc.d/init.d/sapdb-web start\" to start SAP DB WebServer."
fi


%preun web
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/sapdb-web ]; then
		/etc/rc.d/init.d/sapdb-web stop 1>&2
	fi
	/sbin/chkconfig --del sapdb-web
fi

%post precompiler
# register precompiler runtime
X_PATH=%{sapdbdir}/indep_prog/bin
export X_PATH
su sapdb -c "$X_PATH/irconf -i -p %{sapdbdir}/interfaces/precompiler/runtime/7403" >/dev/null 2>&1
exit 0

%preun precompiler
# unregister precompiler runtime
IND_PATH=%{sapdbvar}/indep_data
X_PATH=%{sapdbdir}/indep_prog/bin
export IND_PATH X_PATH
if [ -f $IND_PATH/wrk/irtrace.shm ]; then
	rm -f $IND_PATH/wrk/irtrace.shm
fi
su sapdb -c "$X_PATH/irconf -r -p %{sapdbdir}/interfaces/precompiler/runtime/7403" >/dev/null 2>&1
exit 0

%files docs
%defattr(644,root,root,755)
%doc html
%doc *.pdf

%files ind
%defattr(644,root,root,755)
%lang(de) %doc README.SuSE 
%dir %{sapdbdir}
%dir %{sapdbdir}/indep_prog
%dir %{sapdbdir}/indep_prog/bin
%attr(755,root,root) %{sapdbdir}/indep_prog/bin/*
%{sapdbdir}/indep_prog/env
%{sapdbdir}/indep_prog/etc
%dir %{sapdbdir}/indep_prog/pgm
%attr(755,root,root) %{sapdbdir}/indep_prog/pgm/*
%dir %{sapdbdir}/indep_prog/runtime
%dir %{sapdbdir}/indep_prog/runtime/7403
%dir %{sapdbdir}/indep_prog/runtime/7403/lib
%attr(755,root,root) %{sapdbdir}/indep_prog/runtime/7403/lib/*
%{sapdbdir}/indep_prog/terminfo
%dir %attr(755,sapdb,sapdb) %{sapdbvar}
%attr(644,sapdb,sapdb) %{sapdbvar}/.profile
%dir %attr(775,sapdb,sapdb) %{sapdbvar}/indep_data
%dir %attr(775,sapdb,sapdb) %{sapdbvar}/indep_data/config
%dir %attr(775,sapdb,sapdb) %{sapdbvar}/indep_data/wrk
%dir %attr(775,root,sapdb) %{sqlspool}
%dir %attr(775,root,sapdb) %{sqlspool}/ini
%dir %attr(775,root,sapdb) %{sqlspool}/dbspeed
%dir %attr(775,root,sapdb) %{sqlspool}/diag
%dir %attr(775,root,sapdb) %{sqlspool}/fifo
%dir %attr(775,root,sapdb) %{sqlspool}/ipc
%dir %attr(775,root,sapdb) %{sqlspool}/pid
%dir %attr(775,root,sapdb) %{sqlspool}/ppid
%dir %{sapdbdir}/interfaces

%files srv
%defattr(644,root,root,755)
%dir %{sapdbdir}/depend
%dir %{sapdbdir}/depend/bin
%attr(755,root,root) %{sapdbdir}/depend/bin/*
%{sapdbdir}/depend/env
%{sapdbdir}/depend/etc
%dir %{sapdbdir}/depend/lib
%attr(755,root,root) %{sapdbdir}/depend/lib/*.so
%{sapdbdir}/depend/lib/python1.5
%{_libdir}/python2.2
%dir %{sapdbdir}/depend/misc
%attr(755,root,root) %{sapdbdir}/depend/misc/bgrep
%attr(755,root,root) %{sapdbdir}/depend/misc/get_page
%attr(755,root,root) %{sapdbdir}/depend/misc/patchb
%attr(755,root,root) %{sapdbdir}/depend/misc/pchtab
%attr(755,root,root) %{sapdbdir}/depend/misc/puclst
%attr(755,root,root) %{sapdbdir}/depend/misc/updcol
%attr(755,root,root) %{sapdbdir}/depend/misc/x_watch
%{sapdbdir}/depend/misc/*.py
%dir %{sapdbdir}/depend/misc/sapdb
%{sapdbdir}/depend/misc/sapdb/*.py
%dir %{sapdbdir}/depend/misc/sapdb/pythondef
%attr(755,root,root) %{sapdbdir}/depend/misc/sapdb/pythondef/*.so
%{sapdbdir}/depend/misc/sapdb/pythondef/*.py
%dir %{sapdbdir}/depend/pgm
%attr(755,root,root) %{sapdbdir}/depend/pgm/*
%dir %{sapdbdir}/depend/sap
%attr(755,root,root) %{sapdbdir}/depend/sap/updcol
%{sapdbdir}/depend/sap/grantxdb.dbm
%attr(755,sapdb,sapdb) %{sapdbdir}/depend/wrk
%attr(744,root,root) /etc/rc.d/init.d/sapdb
%config(noreplace) %verify(not size mtime md5) /etc/sysconfig/sapdb
/etc/pam.d/sapdb

%files web
%defattr(644,root,root,755)
%dir %{sapdbdir}/web
%{sapdbdir}/web/Documents
%{sapdbdir}/web/config
%{sapdbdir}/web/env
%dir %{sapdbdir}/web/lib
%attr(755,root,root) %{sapdbdir}/web/lib/*
%dir %{sapdbdir}/web/pgm
%attr(755,root,root) %{sapdbdir}/web/pgm/wahttp
%{sapdbdir}/web/pgm/wahttp.conf
%attr(744,root,root) /etc/rc.d/init.d/sapdb-web
%{sqlspool}/ini/WebAgent74.ini
%dir /var/log/sapdb
%dir /var/run/wahttp

%files precompiler
%defattr(644,root,root,755)
%dir %{sapdbdir}/interfaces/precompiler
%dir %{sapdbdir}/interfaces/precompiler/bin
%attr(755,root,root) %{sapdbdir}/interfaces/precompiler/bin/*
%dir %{sapdbdir}/interfaces/precompiler/runtime
%dir %{sapdbdir}/interfaces/precompiler/runtime/7403
%dir %{sapdbdir}/interfaces/precompiler/runtime/7403/lib
%attr(755,root,root) %{sapdbdir}/interfaces/precompiler/runtime/7403/lib/*
%dir %{sapdbdir}/interfaces/precompiler/sdk
%dir %{sapdbdir}/interfaces/precompiler/sdk/7403
%dir %{sapdbdir}/interfaces/precompiler/sdk/7403/bin
%attr(755,root,root) %{sapdbdir}/interfaces/precompiler/sdk/7403/bin/*
%{sapdbdir}/interfaces/precompiler/sdk/7403/env
%{sapdbdir}/interfaces/precompiler/sdk/7403/incl
%{sapdbdir}/interfaces/precompiler/sdk/7403/lib
%dir %{sapdbdir}/interfaces/precompiler/sdk/7403/pgm
%attr(755,root,roo) %{sapdbdir}/interfaces/precompiler/sdk/7403/pgm/*

%files callif
%defattr(644,root,root,755)
%dir %{sapdbdir}/interfaces/odbc
%{sapdbdir}/interfaces/odbc/env
%{sapdbdir}/interfaces/odbc/incl
%dir %{sapdbdir}/interfaces/odbc/lib
%attr(755,root,root) %{sapdbdir}/interfaces/odbc/lib/*.so
%{sapdbdir}/interfaces/odbc/lib/*.a
%{sapdbdir}/interfaces/jdbc

%files scriptif
%defattr(644,root,root,755)
%dir %{sapdbdir}/interfaces/python
%dir %{sapdbdir}/interfaces/python/misc
%{sapdbdir}/interfaces/python/misc/*.py
%dir %{sapdbdir}/interfaces/python/misc/sapdb
%{sapdbdir}/interfaces/python/misc/sapdb/*.py
%dir %{sapdbdir}/interfaces/python/misc/sapdb/pythondef
%attr(755,root,root) %{sapdbdir}/interfaces/python/misc/sapdb/pythondef/*.so
%{sapdbdir}/interfaces/python/misc/sapdb/pythondef/*.py

%files testdb
%defattr(644,root,root,755)
%dir %{sapdbdir}/testdb
%attr(755,sapdb,sapdb) %{sapdbdir}/testdb/*
