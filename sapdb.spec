
# TODO:
#	- Correct web server pages to work fine with konqueror.
#	- All scripts which use dbmcli look for an exit result grepping
#	  dbmcli output and searching "OK" phrase. It's wrong while error
#	  messages can contains "OK" phrase too.
#	- A sweet dream: dynamic linking...
#	- update /etc/services with following values:
#		sql6		7210/tcp
#		sapdbni72	7269/tcp
#		sql30		7200/tcp

%define		mainver		7.4
%define		subver		3.17
%define		intversion	V74_03_17

Summary:	SAP DB
Summary(pl):	SAP DB
Name:		sapdb
Version:	%{mainver}.%{subver}
Release:	0.6
License:	GPL
Group:		Applications/Databases
Source0:	ftp://ftp.sap.com/pub/sapdb/%{mainver}/sapdb-source-%{mainver}.0%{subver}.tgz
# Source0-md5:	6a2635b0859c0f8f1b02c43fa44b52ff
Source1:	ftp://ftp.sap.com/pub/sapdb/%{mainver}/sapdb-devtools-src.tgz
# Source1-md5:	a0f37f9d099ce25bc586c75179a5a70f
Source2:	ftp://ftp.sap.com/pub/sapdb/%{mainver}/sapdb-htmldoc-%{mainver}.tgz
# Source2-md5:	5f9671d6733cae53d5f7438a3a22eb81
Source3:	%{name}.init
Source4:	%{name}-web.init
Source5:	%{name}-suse-demo.tar.bz2
# Source5-md5:	7087a65261c8e8b35be8bca3531cbb94
Source6:	%{name}-sysconfig
Source8:	%{name}-suse-pam
Source10:	migration73_74eng.pdf
# Source10-md5:	02c2ee8729e456f359e6f098c4a781df
Source12:	%{name}-suse-firststeps.tgz
# Source12-md5:	71c509c36a830f5c56e0fa423fc6a33a
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
Patch22:	%{name}-nostatic-ncurses.patch
Patch23:	%{name}-loadercperl.patch
Patch24:	%{name}-python-dep.patch
URL:		http://www.sapdb.org/
BuildRequires:	bash
BuildRequires:	bison
BuildRequires:	glibc-devel
BuildRequires:	libsigc++12-devel >= 1.2.4
BuildRequires:	ncurses-devel
BuildRequires:	pam-devel
BuildRequires:	perl
BuildRequires:	python >= 2.2
BuildRequires:	python-libs >= 2.2
BuildRequires:	python-devel >= 2.2
BuildRequires:	python-devel-src >= 2.2
BuildRequires:	rpmbuild(macros) >= 1.159
BuildRequires:	vim-static
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		sapdbdir	%{_libdir}/%{name}
%define		sapdbvar	/var/lib/%{name}
%define		sqlspool	/var/spool/sql
%define		depend		%{sapdbdir}/depend
%define		indep		%{sapdbdir}/indep_prog
%define		indepdat	%{sapdbvar}/indep_data
%define		webtools	%{sapdbdir}/web

%define		_noautocompressdoc *.doc

%description
SAP DB.

%description -l pl
SAP DB.

%package docs
Summary:	SAP DB documentation
Summary(pl):	Dokumentacja SAP DB
Group:		Applications/Databases

%description docs
HTML documentation for SAP DB.
For more information please see http://www.sapdb.org/ .

%description docs -l pl
Dokumentacja HTML do SAP DB.
Wiêcej informacji mo¿na znale¼æ na stronie http://www.sapdb.org/ .

%package ind
Summary:	SAP DB - release independend programs
Summary(pl):	SAP DB - programy niezale¿ne od wersji
Group:		Applications/Databases
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(post,postun):	/sbin/chkconfig
Requires:	python >= 2.2
Requires:	python-modules >= 2.2
Provides:	group(sapsys)
Provides:	user(sapdb)

%description ind
- remote communication server
- command line tools for database administration
- precompiler runtime (for applications built by SAP DB precompiler)
For more information please see http://www.sapdb.org/ .

%description ind -l pl
- serwer zdalnego dostêpu
- narzêdzia linii poleceñ do administracji bazami danych
- czê¶æ uruchomieniowa prekompilatora (dla aplikacji zbudowanych przez
  prekompilator SAP DB)
Wiêcej informacji mo¿na znale¼æ na stronie http://www.sapdb.org/ .

%package srv
Summary:	SAP DB database server
Summary(pl):	Serwer bazodanowy SAP DB
Group:		Applications/Databases
Requires(pre):	%{name}-ind = %{version}
Requires(post,postun):	/sbin/chkconfig

%description srv
SAP DB database server.

%description srv -l pl
Serwer bazodanowy SAP DB.

%package web
Summary:	SAP DB web tools
Summary(pl):	Narzêdzia WWW dla SAP DB
Group:		Applications/Databases
Requires:	%{name}-ind = %{version}
Requires:	%{name}-callif >= %{version}

%description web
SAP DB web tools.

%description web -l pl
Narzêdzia WWW dla SAP DB.

%package precompiler
Summary:	SAP DB precompiler
Summary(pl):	Prekompilator SAP DB
Group:		Applications/Databases
PreReq:		sapdb-ind >= %{version}

%description precompiler
SAP DB precompiler.

%description precompiler -l pl
Prekompilator SAP DB.

%package callif
Summary:	SAP DB ODBC and JDBC interfaces
Summary(pl):	Interfejsy ODBC i JDBC do SAP DB
Group:		Applications/Databases
Requires:	%{name}-ind = %{version}

%description callif
- ODBC driver
- JDBC driver
For more information please see http://www.sapdb.org/ .

%description callif -l pl
- sterownik ODBC
- sterownik JDBC
Wiêcej informacji mo¿na znale¼æ na stronie http://www.sapdb.org/ .

%package scriptif
Summary:	SAP DB Perl and Python interfaces
Summary(pl):	Interfejsy Perla i Pythona do SAP DB
Group:		Applications/Databases
PreReq:		sapdb-ind >= %{version}

%description scriptif
SAP DB Perl and Python interfaces.

%description scriptif -l pl
Interfejsy Perla i Pythona do SAP DB.

%package testdb
Summary:	SAP DB test database
Summary:	Testowa baza danych SAP DB
Group:		Applications/Databases
PreReq:		sapdb-ind sapdb-srv

%description testdb
This package contains a script tp create and immediately start
a database instance TST (having 20 MB data space and 8 MB log space).
Please remember to shutdown database before system shutdown.
- sample database user: TEST, password TEST
- DBM user: DBM, password DBM
- database administrator: DBA, password DBA
A script to remove this database is also included.
The scripts can be found in the %{sapdbdir}/testdb directory, and
should be started as user sapdb.

%description testdb -l pl
Ten pakiet zawiera skrypt tp tworz±cy instancjê TST bazy danych
(zawieraj±c± 20 MB miejsca na dane i 8 MB miejsca na logi) i
natychmiast j± uruchamiaj±cy. Nale¿y pamiêtaæ o wy³±czeniu bazy
danych przed zamkniêciem systemu.
- przyk³adowy u¿ytkownik bazy danych: TEST, has³o TEST
- u¿ytkownik DBM: DBM, has³o DBM
- administrator bazy danych: DBA, has³o DBA
Znajduje siê tu równie¿ skrypt usuwaj±cy tê bazê danych.
Skrypty znajduj± siê w katalogu %{sapdbdir}/testdb i powinien je
uruchamiaæ u¿ytkownik sapdb.

%prep
%setup -q -c -a0 -T
mkdir buildtools
tar xzf %{SOURCE1} -C buildtools
tar xzf %{SOURCE2}
mv htmldoc-74 html
tar xzf %{SOURCE12} -C html
bzip2 -dc %{SOURCE5} | tar xf -

cd %{intversion}
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
%patch23 -p1
%patch24 -p1
cd ..

cd buildtools
%patch10 -p1
%patch11
%patch12 -p1
%patch13
%patch14
%patch18
%patch19 -p1
%patch22 -p1

%build
# generate sapdb build tools
chmod -R u+w $RPM_BUILD_DIR/%{name}-%{version}/buildtools
cd $RPM_BUILD_DIR/%{name}-%{version}/buildtools
NOREG=1
export NOREG
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
echo "LD_LIBRARY_PATH=\$INSTROOT/lib:$LD_LIBRARY_PATH export LD_LIBRARY_PATH" >> $IPROF

. $RPM_BUILD_DIR/%{name}-%{version}/%{intversion}/SAPDB_ORG/.iprofile

imf -x all
%ifarch %{ix86} ia64 x86_64
ims -x slowknl
%endif

%install
rm -rf $RPM_BUILD_ROOT

ORG=$RPM_BUILD_DIR/%{name}-%{version}/%{intversion}/SAPDB_ORG

mkdir -p \
    $RPM_BUILD_ROOT/etc/sysconfig \
    $RPM_BUILD_ROOT%{sapdbdir}/{testdb,bin,pgm,sap} \
    $RPM_BUILD_ROOT%{sapdbdir}/misc/sapdb/pythondef \
    $RPM_BUILD_ROOT%{sapdbdir}/runtime/jar \
    $RPM_BUILD_ROOT%{sapdbdir}/runtime/7403/lib \
    $RPM_BUILD_ROOT%{sqlspool}/{dbspeed,diag,fifo,ipc,pid,ppid} \
    $RPM_BUILD_ROOT%{sapdbvar}/{config,wrk} \
    $RPM_BUILD_ROOT%{_libdir}/python2.2 \
    $RPM_BUILD_ROOT%{_includedir}/sapdb

#
# install SAPDB files
#
cp -a $ORG/usr/Documents $RPM_BUILD_ROOT%{sapdbdir}

# bin directory
cp $ORG/usr/bin/{dbanalyzer,dbmcli-HelpInst,dbmcli,irtrace,loadercli,backint} \
    $ORG/usr/bin/{pipe2file,cpc,repmcli,dbmgetf,xuserUnicode,x_ping,sysmon} \
    $ORG/usr/bin/{irconf,cpclnk,buildinfo,sdbinfo,sqlver,sqlwhat,x_look} \
    $ORG/usr/bin/{x_install,op2np,odbclnk,x_genwin,ps_all} \
    $RPM_BUILD_ROOT%{sapdbdir}/bin

for i in x_analys x_clear x_cons x_diagnose x_maketi x_python x_server x_show \
    x_start x_stop x_wiz x_wizard x_wizstop x_wiztrc xbackup xci xdbload \
    xinstinfo xkernprot xoldci xpu xregcomp xsql xsqlpro xsysrc xtracesort \
    xuser xvttest; do
	ln -sf %{sapdbdir}/bin/sysmon $RPM_BUILD_ROOT%{sapdbdir}/bin/$i
done

cat $ORG/usr/bin/ireport.py | sed "s:/usr/bin/env :%{sapdbdir}/bin/:" > \
    $RPM_BUILD_ROOT%{sapdbdir}/bin/ireport.py

# env, terminfo, etc
cp -a $ORG/usr/env $RPM_BUILD_ROOT%{sapdbdir}
cp -a $ORG/usr/etc $RPM_BUILD_ROOT%{sapdbdir}
cp -a $ORG/usr/terminfo $RPM_BUILD_ROOT%{sapdbdir}

# pgm
cp `ls $ORG/usr/pgm | egrep -v "\.f|\.s" | xargs printf "$ORG/usr/pgm/%%s\n"` \
    $RPM_BUILD_ROOT%{sapdbdir}/pgm
ln -sf /usr/bin/python $RPM_BUILD_ROOT%{sapdbdir}/pgm/python

# lib
cp `ls $ORG/usr/lib/*.so` $RPM_BUILD_ROOT%{_libdir}
ln -sf %{_libdir} $RPM_BUILD_ROOT%{sapdbdir}/lib
cp $ORG/usr/lib/python1.5/* $RPM_BUILD_ROOT%{_libdir}/python2.2
ln -sf %{_libdir}/python2.2 $RPM_BUILD_ROOT%{_libdir}/python1.5

# misc
cp -a $ORG/usr/misc/DBD $RPM_BUILD_ROOT%{sapdbdir}/misc
cp -a $ORG/usr/misc/SAP $RPM_BUILD_ROOT%{sapdbdir}/misc
cp `ls $ORG/usr/misc/*.txt` \
    $RPM_BUILD_ROOT%{sapdbdir}/misc
cp `ls $ORG/usr/misc/sapdb/*.py` \
    $RPM_BUILD_ROOT%{sapdbdir}/misc/sapdb
cp `ls $ORG/usr/misc/sapdb/pythondef/*.py` \
    `ls $ORG/usr/misc/sapdb/pythondef/*.so` \
    $RPM_BUILD_ROOT%{sapdbdir}/misc/sapdb/pythondef
cp `ls $ORG/usr/misc/*.so` `ls $ORG/usr/misc/*.py` \
    $ORG/usr/misc/{updcol,puclst,pchtab,get_page,instperl.pl,bgrep,patchb,x_watch} \
    $RPM_BUILD_ROOT%{sapdbdir}/misc

# config
sed 's:$OWN32:%{sapdbdir}/web:g
s:$OWN64:%{sapdbdir}/web:g
s:$LOG:/var/log/sapdb:g
s:Port=85:Port=9999:g' $ORG/usr/config/WebAgent74.ini \
    > $RPM_BUILD_ROOT%{sapdbvar}/config/WebAgent74.ini
cp $ORG/usr/config/{mime.types,instweb} $RPM_BUILD_ROOT%{sapdbvar}/config
ln -sf %{sapdbvar}/config $RPM_BUILD_ROOT%{sapdbdir}/config
ln -sf %{sapdbvar}/config $RPM_BUILD_ROOT%{sqlspool}/ini

# runtime
cp $ORG/usr/runtime/jar/* $RPM_BUILD_ROOT%{sapdbdir}/runtime/jar
cp $ORG/usr/runtime/7403/lib/libpcr.so $RPM_BUILD_ROOT%{sapdbdir}/runtime/7403/lib

# sap
cp `ls $ORG/usr/sap | egrep -v "\.f|\.a" | xargs printf "$ORG/usr/sap/%%s\n"` \
    $RPM_BUILD_ROOT%{sapdbdir}/sap
ln -sf %{sapdbdir}/misc/updcol $RPM_BUILD_ROOT%{sapdbdir}/updcol

# sdk
FILES=`find $ORG/usr/sdk -type f -printf "%%P\n" | grep -v "\.f"`
for f in $FILES; do
    mkdir -p $RPM_BUILD_ROOT%{sapdbdir}/sdk/`dirname $f`
    cp $ORG/usr/sdk/$f $RPM_BUILD_ROOT%{sapdbdir}/sdk/$f
done

# incl
cp -a $ORG/usr/incl/* $RPM_BUILD_ROOT%{_includedir}/sapdb
mv $RPM_BUILD_ROOT%{sapdbdir}/sdk/7403/incl/* \
    $RPM_BUILD_ROOT%{_includedir}/sapdb
rm -rf $RPM_BUILD_ROOT%{sapdbdir}/sdk/7403/incl
ln -sf %{_includedir}/sapdb $RPM_BUILD_ROOT%{sapdbdir}/sdk/7403/incl

# wrk
ln -sf %{sapdbvar}/wrk $RPM_BUILD_ROOT%{sapdbdir}/wrk

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
rm -rf migration73_74eng.pdf
cp %{SOURCE10}	$RPM_BUILD_DIR/%{name}-%{version}

#
# depend/indep_prog/indep_data structure
#
install -d $RPM_BUILD_ROOT%{depend}
ln -sf %{sapdbdir}/bin $RPM_BUILD_ROOT%{depend}/bin
ln -sf %{sapdbdir}/lib $RPM_BUILD_ROOT%{depend}/lib
ln -sf %{sapdbdir}/env $RPM_BUILD_ROOT%{depend}/env
ln -sf %{sapdbdir}/etc $RPM_BUILD_ROOT%{depend}/etc
ln -sf %{sapdbdir}/pgm $RPM_BUILD_ROOT%{depend}/pgm
ln -sf %{sapdbdir}/sap $RPM_BUILD_ROOT%{depend}/sap
ln -sf %{sapdbdir}/wrk $RPM_BUILD_ROOT%{depend}/wrk
ln -sf %{sapdbdir}/misc $RPM_BUILD_ROOT%{depend}/misc

install -d $RPM_BUILD_ROOT%{webtools}
ln -sf %{sapdbdir}/Documents $RPM_BUILD_ROOT%{webtools}/Documents
ln -sf %{sapdbvar}/config $RPM_BUILD_ROOT%{webtools}/config
ln -sf %{sapdbdir}/env $RPM_BUILD_ROOT%{webtools}/env
ln -sf %{sapdbdir}/lib $RPM_BUILD_ROOT%{webtools}/lib
ln -sf %{sapdbdir}/pgm $RPM_BUILD_ROOT%{webtools}/pgm

install -d $RPM_BUILD_ROOT%{indep}
ln -sf %{sapdbdir}/bin $RPM_BUILD_ROOT%{indep}/bin
ln -sf %{sapdbdir}/env $RPM_BUILD_ROOT%{indep}/env
ln -sf %{sapdbdir}/etc $RPM_BUILD_ROOT%{indep}/etc
ln -sf %{_includedir}/%{name} $RPM_BUILD_ROOT%{indep}/incl
ln -sf %{sapdbdir}/lib $RPM_BUILD_ROOT%{indep}/lib
ln -sf %{sapdbdir}/misc $RPM_BUILD_ROOT%{indep}/misc
ln -sf %{sapdbdir}/pgm $RPM_BUILD_ROOT%{indep}/pgm
ln -sf %{sapdbdir}/runtime $RPM_BUILD_ROOT%{indep}/runtime
ln -sf %{sapdbdir}/sdk $RPM_BUILD_ROOT%{indep}/sdk
ln -sf %{sapdbdir}/terminfo $RPM_BUILD_ROOT%{indep}/terminfo
ln -sf %{webtools} $RPM_BUILD_ROOT%{indep}/web

install -d $RPM_BUILD_ROOT%{indepdat}
ln -sf %{sapdbvar}/wrk $RPM_BUILD_ROOT%{indepdat}/wrk
ln -sf %{sapdbvar}/config $RPM_BUILD_ROOT%{indepdat}/config

#
# sapdb user HOME scripts
#
cat <<EOF > $RPM_BUILD_ROOT%{sapdbvar}/.profile
INDEP=%{indep}
DEP=%{depend}

SAPDBROOT=\$DEP
PATH=\$PATH:\$IND/bin:\$DEP/bin
#CLASSPATH=\$CLASSPATH:\$SAPDBROOT/misc/sapdbc.jar:.
#PERL5LIB=\$PERL5LIB:\$SAPDBROOT/misc
#PYTHONPATH=\$PYTHONPATH:\$SAPDBROOT/misc

export INDEP DEP SAPDBROOT PATH
#export PYTHONPATH
#export CLASSPATH
#export PERL5LIB
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%pre ind
if [ -n "`/usr/bin/getgid sapsys`" ]; then
	if [ "`/usr/bin/getgid sapsys`" != "101" ]; then
		echo "Error: group sapsys doesn't have gid=101. Correct this before installing sapdb." 1>&2
		exit 1
	fi
else
	/usr/sbin/groupadd -g 101 sapsys 1>&2
fi

if [ -n "`/bin/id -u sapdb 2>/dev/null`" ]; then
	if [ "`/bin/id -u sapdb`" != "101" ]; then
		echo "Error: user sapdb doesn't have uid=101. Correct this before installing sapdb." 1>&2
		exit 1
	fi
else
	/usr/sbin/useradd -u 101 -g sapsys -d %{sapdbvar} -s /bin/bash \
		-c "SAP DB" sapdb 1>&2
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

DBROOT=%{indep}
export DBROOT

o=`$DBROOT/bin/dbmcli -s dbm_setpath IndepDataPath %{indepdat}`
t=`echo $o | grep OK`
if [ "$t" = "" ]; then
	echo "- could not set inpedendent data path: $o" >&2
	exit 1
fi

o=`$DBROOT/bin/dbmcli -s dbm_setpath IndepProgPath %{indep}`
t=`echo $o | grep OK`
if [ "$t" = "" ]; then
	echo "- could not set independent program path: $o" >&2
	exit 1
fi
chown sapdb:sapsys %{sqlspool}/ini/SAP_DBTech.ini

#register precompiler runtime
%{indep}/bin/irconf -i -p %{indep}/runtime/7403 >/dev/null 2>&1 || :
%{indep}/bin/irconf -i -p %{indep}/runtime/7300 >/dev/null 2>&1 || :
%{indep}/bin/irconf -i -p %{indep}/runtime/7250 >/dev/null 2>&1 || :
%{indep}/bin/irconf -i -p %{indep}/runtime/7240 >/dev/null 2>&1 || :
exit 0

%preun ind
%{indep}/bin/irconf -r -p %{indep}/runtime/7403 >/dev/null 2>&1 || :
%{indep}/bin/irconf -r -p %{indep}/runtime/7300 >/dev/null 2>&1 || :
%{indep}/bin/irconf -r -p %{indep}/runtime/7250 >/dev/null 2>&1 || :
%{indep}/bin/irconf -r -p %{indep}/runtime/7240 >/dev/null 2>&1 || :

if [ "$1" != "0" ]; then
	# do nothing in upgrade case
	exit 0
fi

DBROOT=%{indep}
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

rm -rf %{indepdat}/wrk/_OPTSAPD >/dev/null 2>&1
rm -f %{indepdat}/wrk/dbmsrv.prt >/dev/null 2>&1
rm -f %{indepdat}/config/_OPTSAPD* >/dev/null 2>&1
rm -f %{indepdat}/wrk/vserver.prot >/dev/null 2>&1
rm -f %{sqlspool}/ini/SAP_DBTech.ini* > /dev/null 2>&1
rm -rf %{indepdat}/wrk/irtrace* >/dev/null 2>&1
rm -f %{indepdat}/config/Registry1.dcom >/dev/null 2>&1
rm -f %{sqlspool}/ini/Registry_dcom.ini >/dev/null 2>&1
rm -rf %{indepdat}/wrk/root >/dev/null 2>&1
exit 0

%postun ind
if [ "$1" = "0" ] ; then
	%userremove sapdb
	%groupremove sapsys
fi

%post srv
/sbin/chkconfig --add sapdb
if [ -f /var/lock/subsys/sapdb ]; then
	/etc/rc.d/init.d/sapdb restart 1>&2
else
	echo "Run \"/etc/rc.d/init.d/sapdb start\" to start SAP DB."
fi

DBROOT=%{depend}
export DBROOT

o=`su - sapdb -c "umask 0003; $DBROOT/bin/dbmcli -s -R $DBROOT inst_reg -k $DBROOT"`
t=`echo $o | grep OK`
if [ "$t" = "" ]; then
	echo "- could not register the installation: $o" >&2
	exit 1
fi

dcom_link=%{depend}/wrk/Registry.dcom
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
chown sapdb:sapsys %{sapdbvar}/config/Registry1.dcom

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

DBROOT=%{depend}
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
rm -f %{indepdat}/config/Registry1.dcom >/dev/null 2>&1
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
X_PATH=%{indep}/bin
export X_PATH
su sapdb -c "$X_PATH/irconf -i -p %{sapdbdir}/interfaces/precompiler/runtime/7403" >/dev/null 2>&1
exit 0

%preun precompiler
# unregister precompiler runtime
IND_PATH=%{indepdat}
X_PATH=%{indep}/bin
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
%defattr(644,sapdb,sapsys,755)
%dir %{indep}
%{indep}/*
%dir %{indepdat}
%{indepdat}/*
%dir %{sapdbdir}
%dir %{sapdbdir}/bin
%attr(755,sapdb,sapsys) %{sapdbdir}/bin/dbanalyzer
%attr(755,sapdb,sapsys) %{sapdbdir}/bin/dbmcli
%attr(755,sapdb,sapsys) %{sapdbdir}/bin/dbmgetf
%attr(755,sapdb,sapsys) %{sapdbdir}/bin/irconf
%attr(755,sapdb,sapsys) %{sapdbdir}/bin/ireport.py
%attr(755,sapdb,sapsys) %{sapdbdir}/bin/ps_all
%attr(755,sapdb,sapsys) %{sapdbdir}/bin/sdbinfo
%attr(755,sapdb,sapsys) %{sapdbdir}/bin/sysmon
%attr(755,sapdb,sapsys) %{sapdbdir}/bin/x_analys
%attr(755,sapdb,sapsys) %{sapdbdir}/bin/x_cons
%attr(755,sapdb,sapsys) %{sapdbdir}/bin/x_maketi
%attr(755,sapdb,sapsys) %{sapdbdir}/bin/x_server
%attr(755,sapdb,sapsys) %{sapdbdir}/bin/x_wiz
%attr(755,sapdb,sapsys) %{sapdbdir}/bin/x_wizstop
%attr(755,sapdb,sapsys) %{sapdbdir}/bin/xsysrc
%attr(755,sapdb,sapsys) %{sapdbdir}/bin/xuser
%attr(755,sapdb,sapsys) %{sapdbdir}/bin/xuserUnicode
%attr(755,sapdb,sapsys) %{sapdbdir}/bin/xvttest
%{sapdbdir}/lib
%attr(755,sapdb,sapsys) %{_libdir}/libsqlrte-nouniqueid.so
%attr(755,sapdb,sapsys) %{_libdir}/libsqlrte.so
%dir %{sapdbdir}/env
%{sapdbdir}/env/*.cfg
%{sapdbdir}/env/vserver.use
%{sapdbdir}/etc
%dir %{sapdbdir}/pgm
%attr(755,sapdb,sapsys) %{sapdbdir}/pgm/maketi
%attr(755,sapdb,sapsys) %{sapdbdir}/pgm/vserver
%attr(755,sapdb,sapsys) %{sapdbdir}/pgm/vttest
%dir %{sapdbdir}/runtime
%dir %{sapdbdir}/runtime/7403
%dir %{sapdbdir}/runtime/7403/lib
%attr(755,sapdb,sapsys) %{sapdbdir}/runtime/7403/lib/*
%{sapdbdir}/terminfo
%attr(644,sapdb,sapsys) %{sapdbvar}/.profile
%dir %attr(775,sapdb,sapsys) %{sapdbvar}
%dir %attr(775,sapdb,sapsys) %{sapdbvar}/config
%dir %attr(775,sapdb,sapsys) %{sapdbvar}/wrk
%{sapdbdir}/wrk
%dir %attr(775,sapdb,sapsys) %{sqlspool}
%{sqlspool}/ini
%dir %attr(775,sapdb,sapsys) %{sqlspool}/dbspeed
%dir %attr(775,sapdb,sapsys) %{sqlspool}/diag
%dir %attr(775,sapdb,sapsys) %{sqlspool}/fifo
%dir %attr(775,sapdb,sapsys) %{sqlspool}/ipc
%dir %attr(775,sapdb,sapsys) %{sqlspool}/pid
%dir %attr(775,sapdb,sapsys) %{sqlspool}/ppid

%files srv
%defattr(644,sapdb,sapsys,755)
%dir %{depend}
%{depend}/*
%doc %{sapdbdir}/misc/*.txt
%dir %{sapdbdir}/bin
%attr(755,sapdb,sapsys) %{sapdbdir}/bin/backint
%attr(755,sapdb,sapsys) %{sapdbdir}/bin/dbmcli
%attr(755,sapdb,sapsys) %{sapdbdir}/bin/loadercli
%attr(755,sapdb,sapsys) %{sapdbdir}/bin/op2np
%attr(755,sapdb,sapsys) %{sapdbdir}/bin/pipe2file
%attr(755,sapdb,sapsys) %{sapdbdir}/bin/ps_all
%attr(755,sapdb,sapsys) %{sapdbdir}/bin/repmcli
%attr(755,sapdb,sapsys) %{sapdbdir}/bin/sqlver
%attr(755,sapdb,sapsys) %{sapdbdir}/bin/x_diagnose
%attr(755,sapdb,sapsys) %{sapdbdir}/bin/x_ping
%attr(755,sapdb,sapsys) %{sapdbdir}/bin/x_python
%attr(755,sapdb,sapsys) %{sapdbdir}/bin/xdbload
%attr(755,sapdb,sapsys) %{sapdbdir}/bin/xkernprot
%attr(755,sapdb,sapsys) %{sapdbdir}/bin/xregcomp
%attr(755,sapdb,sapsys) %{sapdbdir}/bin/xsql
%attr(755,sapdb,sapsys) %{sapdbdir}/bin/xtracesort
%attr(755,sapdb,sapsys) %{sapdbdir}/bin/buildinfo
%attr(755,sapdb,sapsys) %{sapdbdir}/bin/dbmcli-HelpInst
%attr(755,sapdb,sapsys) %{sapdbdir}/bin/odbclnk
%attr(755,sapdb,sapsys) %{sapdbdir}/bin/x_genwin
%attr(755,sapdb,sapsys) %{sapdbdir}/bin/x_install
%attr(755,sapdb,sapsys) %{sapdbdir}/bin/x_look
%{sapdbdir}/env/*.py
%{sapdbdir}/env/*.pcf
%{sapdbdir}/env/general.use
%{sapdbdir}/env/kernprot.use
%{sapdbdir}/env/regcomp.use
%{sapdbdir}/env/xstart.use
%{sapdbdir}/env/xstop.use
%{sapdbdir}/env/de/PRECOMM.de
%{sapdbdir}/env/de/SQL*.de
%{sapdbdir}/env/en/PRECOMM.en
%{sapdbdir}/env/en/DBM.en
%{sapdbdir}/env/en/SQL*.en
%{sapdbdir}/env/en/REPM.en
%attr(755,sapdb,sapsys) %{_libdir}/ContentStorage.so
%attr(755,sapdb,sapsys) %{_libdir}/dbpinstall.so
%attr(755,sapdb,sapsys) %{_libdir}/liboms.so
%attr(755,sapdb,sapsys) %{_libdir}/libomssimul.so
%attr(755,sapdb,sapsys) %{_libdir}/libsqlcls.so
%{_libdir}/python1.5
%{_libdir}/python2.2
%dir %{sapdbdir}/misc
%attr(755,sapdb,sapsys) %{sapdbdir}/misc/bgrep
%attr(755,sapdb,sapsys) %{sapdbdir}/misc/get_page
%attr(755,sapdb,sapsys) %{sapdbdir}/misc/instperl.pl
%attr(755,sapdb,sapsys) %{sapdbdir}/misc/patchb
%attr(755,sapdb,sapsys) %{sapdbdir}/misc/pchtab
%attr(755,sapdb,sapsys) %{sapdbdir}/misc/puclst
%attr(755,sapdb,sapsys) %{sapdbdir}/misc/updcol
%attr(755,sapdb,sapsys) %{sapdbdir}/misc/x_watch
#%{sapdbdir}/misc/DBD
%{sapdbdir}/misc/SAP
%{sapdbdir}/misc/*.py
%attr(755,sapdb,sapsys) %{sapdbdir}/misc/*.so
%dir %{sapdbdir}/misc/sapdb
%{sapdbdir}/misc/sapdb/*.py
%dir %{sapdbdir}/misc/sapdb/pythondef
%attr(755,sapdb,sapsys) %{sapdbdir}/misc/sapdb/pythondef/*.so
%{sapdbdir}/misc/sapdb/pythondef/*.py
%dir %{sapdbdir}/pgm
%attr(755,sapdb,sapsys) %{sapdbdir}/pgm/console
%attr(755,sapdb,sapsys) %{sapdbdir}/pgm/dbmext
%attr(755,root,sapsys) %{sapdbdir}/pgm/dbmsrv
%attr(755,sapdb,sapsys) %{sapdbdir}/pgm/diagnose
%attr(755,sapdb,sapsys) %{sapdbdir}/pgm/dumpcomreg
%attr(755,sapdb,sapsys) %{sapdbdir}/pgm/kernel
%attr(755,root,sapsys) %{sapdbdir}/pgm/lserver
%attr(755,sapdb,sapsys) %{sapdbdir}/pgm/pu
%attr(755,sapdb,sapsys) %{sapdbdir}/pgm/python
%attr(755,sapdb,sapsys) %{sapdbdir}/pgm/regcomp
%attr(755,sapdb,sapsys) %{sapdbdir}/pgm/slowknl
%attr(755,sapdb,sapsys) %{sapdbdir}/pgm/sqlfilter
%attr(755,sapdb,sapsys) %{sapdbdir}/pgm/sysrc
%attr(755,sapdb,sapsys) %{sapdbdir}/pgm/tracesort
%attr(755,sapdb,sapsys) %{sapdbdir}/pgm/backup
%attr(755,sapdb,sapsys) %{sapdbdir}/pgm/clr_kernel
%attr(755,sapdb,sapsys) %{sapdbdir}/pgm/clr_ps_ipc
%attr(755,sapdb,sapsys) %{sapdbdir}/pgm/cr_param
%attr(755,sapdb,sapsys) %{sapdbdir}/pgm/decompr
%attr(755,sapdb,sapsys) %{sapdbdir}/pgm/getparam
%attr(755,sapdb,sapsys) %{sapdbdir}/pgm/idl2xml
%attr(755,sapdb,sapsys) %{sapdbdir}/pgm/odbcreg
%attr(755,sapdb,sapsys) %{sapdbdir}/pgm/omststknl
%attr(755,sapdb,sapsys) %{sapdbdir}/pgm/putparam
%attr(755,sapdb,sapsys) %{sapdbdir}/pgm/renparam
%attr(755,sapdb,sapsys) %{sapdbdir}/pgm/slowci
%attr(755,sapdb,sapsys) %{sapdbdir}/pgm/sqlfiltern
%attr(755,sapdb,sapsys) %{sapdbdir}/pgm/start
%attr(755,sapdb,sapsys) %{sapdbdir}/pgm/stop
%attr(755,sapdb,sapsys) %{sapdbdir}/pgm/userx
%attr(755,sapdb,sapsys) %{sapdbdir}/pgm/wizard
%attr(755,sapdb,sapsys) %{sapdbdir}/pgm/xml2ispc
%dir %{sapdbdir}/sap
%attr(755,sapdb,sapsys) %{sapdbdir}/sap/lcinit
%attr(755,sapdb,sapsys) %{sapdbdir}/sap/niping
%{sapdbdir}/sap/updcol
%{sapdbdir}/sap/*.dbm
%{sapdbdir}/sap/*.lst
%attr(755,sapdb,sapsys) %{sapdbdir}/sap/*.so
%attr(744,sapdb,sapsys) /etc/rc.d/init.d/sapdb
%config(noreplace) %verify(not size mtime md5) /etc/sysconfig/sapdb
%{sapdbdir}/etc
/etc/pam.d/sapdb

%files web
%defattr(644,sapdb,sapsys,755)
%dir %{webtools}
%{webtools}/*
%dir %{sapdbdir}
%{sapdbdir}/Documents
%{sapdbdir}/config
%{sapdbdir}/env/webdav.ins
%attr(755,sapdb,sapsys) %{_libdir}/libdbfsapi.so
%attr(755,sapdb,sapsys) %{_libdir}/libwapi.so
%attr(755,sapdb,sapsys) %{_libdir}/libwdvcapi.so
%attr(755,sapdb,sapsys) %{_libdir}/libwdvhandler.so
%attr(755,sapdb,sapsys) %{_libdir}/waecho.so
%attr(755,sapdb,sapsys) %{_libdir}/webdbm.so
%attr(755,sapdb,sapsys) %{_libdir}/websql.so
%attr(755,sapdb,sapsys) %{sapdbdir}/pgm/wahttp
%{sapdbdir}/pgm/wahttp.conf
%attr(744,sapdb,sapsys) /etc/rc.d/init.d/sapdb-web
%{sqlspool}/ini
%dir %attr(770,sapdb,sapsys) /var/log/sapdb
%dir /var/run/wahttp
%{sapdbvar}/config/*.ini
%{sapdbvar}/config/mime.types
%attr(755,sapdb,sapsys) %{sapdbvar}/config/instweb

%files precompiler
%defattr(644,sapdb,sapsys,755)
%dir %{sapdbdir}/sdk
%dir %{sapdbdir}/sdk/7403
%dir %{sapdbdir}/sdk/7403/bin
%attr(755,sapdb,sapsys) %{sapdbdir}/sdk/7403/bin/*
%attr(755,sapdb,sapsys) %{sapdbdir}/bin/cpc
%attr(755,sapdb,sapsys) %{sapdbdir}/bin/cpclnk
%attr(755,sapdb,sapsys) %{sapdbdir}/bin/irtrace
%attr(755,sapdb,sapsys) %{sapdbdir}/bin/sqlver
%attr(755,sapdb,sapsys) %{sapdbdir}/bin/sqlwhat
%{sapdbdir}/sdk/7403/env
%{sapdbdir}/sdk/7403/incl
%{sapdbdir}/sdk/7403/lib
%dir %{sapdbdir}/sdk/7403/pgm
%attr(755,sapdb,sapsys) %{sapdbdir}/sdk/7403/pgm/*
%{_includedir}/sapdb

%files callif
%defattr(644,sapdb,sapsys,755)
%{sapdbdir}/runtime/jar
%attr(755,sapdb,sapsys) %{_libdir}/libodcompr.so
%attr(755,sapdb,sapsys) %{_libdir}/libsqlod.so
%{sapdbdir}/env/de/ODBCM.de
%{sapdbdir}/env/en/ODBCM.en

%files scriptif
%defattr(644,sapdb,sapsys,755)
%{sapdbdir}/misc/dbm.py
%{sapdbdir}/misc/loader.py
%{sapdbdir}/misc/repman.py
%{sapdbdir}/misc/sapdbapi.py
%{sapdbdir}/misc/sapdb/__init__.py
%{sapdbdir}/misc/sapdb/dbapi.py
%{sapdbdir}/misc/sapdb/dbm.py
%{sapdbdir}/misc/sapdb/loader.py
%{sapdbdir}/misc/sapdb/sql.py
%{sapdbdir}/misc/sapdb/pythondef/__init__.py
%attr(755,sapdb,sapsys) %{sapdbdir}/misc/sapdb/pythondef/*.so

%files testdb
%defattr(644,sapdb,sapsys,755)
%dir %{sapdbdir}/testdb
%attr(755,sapdb,sapsys) %{sapdbdir}/testdb/*
