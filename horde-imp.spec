%define	module	imp
%define	name	horde-%{module}
%define version 4.3.4
%define release %mkrel 1

%define _requires_exceptions pear(\\(Horde.*\\|Text/Flowed.php\\|VFS.*\\))

Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:	The Horde Internet Messaging Program
License:	GPL
Group:		System/Servers
URL:		http://www.horde.org/%{module}
Source0:	ftp://ftp.horde.org/pub/%{module}/%{module}-h3-%{version}.tar.gz
Patch:      imp-h3-4.3-fix-constant-loading.patch
Requires(post):	rpm-helper
Requires:	horde >= 3.0
Requires:	php-imap
Requires:	php-ldap
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}

%description
IMP is the Internet Messaging Program, one of the Horde applications.
It provides webmail access to IMAP and POP3 accounts.

%prep
%setup -q -n %{module}-h3-%{version}
%patch -p 1

# fix perms
chmod 644 locale/da_DK/help.xml

%build

%install
rm -rf %{buildroot}

# horde configuration
install -d -m 755 %{buildroot}%{_sysconfdir}/horde/registry.d
cat > %{buildroot}%{_sysconfdir}/horde/registry.d/%{module}.php <<'EOF'
<?php
//
// Imp Horde configuration file
//
 
$this->applications['imp'] = array(
    'fileroot' => $this->applications['horde']['fileroot'] . '/imp',
    'webroot'  => $this->applications['horde']['webroot'] . '/imp',
    'name'     => _("Mail"),
    'status'   => 'active',
    'provides' => array('mail', 'contacts/favouriteRecipients')
);

$this->applications['imp-folders'] = array(
    'status'      => 'block',
    'app'         => 'imp',
    'blockname'   => 'tree_folders',
    'menu_parent' => 'imp'
);
EOF

# remove .htaccess files
find . -name .htaccess -exec rm -f {} \;

# install files
install -d -m 755 %{buildroot}%{_var}/www/horde/%{module}
install -d -m 755 %{buildroot}%{_datadir}/horde/%{module}
install -d -m 755 %{buildroot}%{_sysconfdir}/horde
cp -pR *.php %{buildroot}%{_var}/www/horde/%{module}
cp -pR themes %{buildroot}%{_var}/www/horde/%{module}
cp -pR js %{buildroot}%{_var}/www/horde/%{module}
cp -pR lib %{buildroot}%{_datadir}/horde/%{module}
cp -pR locale %{buildroot}%{_datadir}/horde/%{module}
cp -pR scripts %{buildroot}%{_datadir}/horde/%{module}
cp -pR templates %{buildroot}%{_datadir}/horde/%{module}
cp -pR config %{buildroot}%{_sysconfdir}/horde/%{module}

# use symlinks to recreate original structure
pushd %{buildroot}%{_var}/www/horde/%{module}
ln -s ../../../..%{_sysconfdir}/horde/%{module} config
ln -s ../../../..%{_datadir}/horde/%{module}/lib .
ln -s ../../../..%{_datadir}/horde/%{module}/locale .
ln -s ../../../..%{_datadir}/horde/%{module}/templates .
popd
pushd %{buildroot}%{_datadir}/horde/%{module}
ln -s ../../../..%{_sysconfdir}/horde/%{module} config
popd

# activate configuration files
for file in %{buildroot}%{_sysconfdir}/horde/%{module}/*.dist; do
	mv $file ${file%.dist}
done

# fix script shellbang
for file in `find %{buildroot}%{_datadir}/horde/%{module}/scripts`; do
	perl -pi -e 's|/usr/local/bin/php|/usr/bin/php|' $file
done

%clean
rm -rf %{buildroot}

%post
if [ $1 = 1 ]; then
	# configuration
	%create_ghostfile %{_sysconfdir}/horde/%{module}/conf.php apache apache 644
	%create_ghostfile %{_sysconfdir}/horde/%{module}/conf.php.bak apache apache 644
fi

%files
%defattr(-,root,root)
%doc README COPYING docs
%config(noreplace) %{_sysconfdir}/horde/registry.d/%{module}.php
%config(noreplace) %{_sysconfdir}/horde/%{module}
%{_datadir}/horde/%{module}
%{_var}/www/horde/%{module}
