%define	module	imp
%define	name	horde-%{module}
%define version 4.3.9
%define release: 3

%define _requires_exceptions pear(\\(Horde.*\\|Text/Flowed.php\\|VFS.*\\))

Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:	The Horde Internet Messaging Program
License:	GPL
Group:		System/Servers
URL:		http://www.horde.org/%{module}
Source0:	ftp://ftp.horde.org/pub/%{module}/%{module}-h3-%{version}.tar.gz
Patch0:      	imp-h3-4.3-fix-constant-loading.patch
Requires(post):	rpm-helper
Requires:	horde >= 3.3.8
Requires:	php-imap
Requires:	php-ldap
BuildArch:	noarch

%description
IMP is the Internet Messaging Program, one of the Horde applications.
It provides webmail access to IMAP and POP3 accounts.

%prep
%setup -q -n %{module}-h3-%{version}
%patch0 -p 1

# fix perms
chmod 644 locale/da_DK/help.xml

%build

%install
rm -rf %{buildroot}

# apache configuration
install -d -m 755 %{buildroot}%{_webappconfdir}
cat > %{buildroot}%{_webappconfdir}/%{name}.conf <<EOF
# %{name} Apache configuration file

<Directory %{_datadir}/horde/%{module}/lib>
    Order allow,deny
    Deny from all
</Directory>

<Directory %{_datadir}/horde/%{module}/locale>
    Order allow,deny
    Deny from all
</Directory>

<Directory %{_datadir}/horde/%{module}/scripts>
    Order allow,deny
    Deny from all
</Directory>

<Directory %{_datadir}/horde/%{module}/templates>
    Order allow,deny
    Deny from all
</Directory>
EOF

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
?>
EOF

# remove .htaccess files
find . -name .htaccess -exec rm -f {} \;

# install files
install -d -m 755 %{buildroot}%{_datadir}/horde/%{module}
cp -pR *.php %{buildroot}%{_datadir}/horde/%{module}
cp -pR themes %{buildroot}%{_datadir}/horde/%{module}
cp -pR js %{buildroot}%{_datadir}/horde/%{module}
cp -pR lib %{buildroot}%{_datadir}/horde/%{module}
cp -pR locale %{buildroot}%{_datadir}/horde/%{module}
cp -pR scripts %{buildroot}%{_datadir}/horde/%{module}
cp -pR templates %{buildroot}%{_datadir}/horde/%{module}

install -d -m 755 %{buildroot}%{_sysconfdir}/horde
cp -pR config %{buildroot}%{_sysconfdir}/horde/%{module}
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
%if %mdkversion < 201010
%_post_webapp
%endif


%files
%defattr(-,root,root)
%doc README COPYING docs
%config(noreplace) %{_webappconfdir}/%{name}.conf
%config(noreplace) %{_sysconfdir}/horde/registry.d/%{module}.php
%config(noreplace) %{_sysconfdir}/horde/%{module}
%{_datadir}/horde/%{module}


%changelog
* Sat Jun 25 2011 Guillaume Rousse <guillomovitch@mandriva.org> 4.3.9-1mdv2011.0
+ Revision: 687152
- new version

* Sun Aug 08 2010 Thomas Spuhler <tspuhler@mandriva.org> 4.3.7-1mdv2011.0
+ Revision: 567491
- Updated to version 4.3.7
- added version 4.3.6 source file

* Tue Aug 03 2010 Thomas Spuhler <tspuhler@mandriva.org> 4.3.6-3mdv2011.0
+ Revision: 565213
- Increased release for rebuild

* Mon Jan 18 2010 Guillaume Rousse <guillomovitch@mandriva.org> 4.3.6-2mdv2010.1
+ Revision: 493346
- rely on filetrigger for reloading apache configuration begining with 2010.1, rpm-helper macros otherwise

* Sat Dec 26 2009 Funda Wang <fwang@mandriva.org> 4.3.6-1mdv2010.1
+ Revision: 482412
- new version 4.3.6

  + Guillaume Rousse <guillomovitch@mandriva.org>
    - restrict default access permissions to localhost only, as per new policy

* Tue Sep 15 2009 Guillaume Rousse <guillomovitch@mandriva.org> 4.3.5-1mdv2010.0
+ Revision: 443241
- new version
- new simpler files setup

* Wed Aug 26 2009 Guillaume Rousse <guillomovitch@mandriva.org> 4.3.4-1mdv2010.0
+ Revision: 421440
- new version

* Fri Jan 30 2009 Guillaume Rousse <guillomovitch@mandriva.org> 4.3.3-1mdv2009.1
+ Revision: 335510
- new version

* Mon Jan 26 2009 Guillaume Rousse <guillomovitch@mandriva.org> 4.3.2-1mdv2009.1
+ Revision: 333747
- update to new version 4.3.2

* Tue Jan 06 2009 Guillaume Rousse <guillomovitch@mandriva.org> 4.3.1-2mdv2009.1
+ Revision: 326412
- fix apache config file

* Sun Dec 14 2008 Guillaume Rousse <guillomovitch@mandriva.org> 4.3.1-1mdv2009.1
+ Revision: 314355
- update to new version 4.3.1

* Tue Nov 18 2008 Guillaume Rousse <guillomovitch@mandriva.org> 4.3-3mdv2009.1
+ Revision: 304321
- fix constant loading

* Sun Oct 19 2008 Guillaume Rousse <guillomovitch@mandriva.org> 4.3-2mdv2009.1
+ Revision: 295327
- cosmetics

* Sun Oct 19 2008 Guillaume Rousse <guillomovitch@mandriva.org> 4.3-1mdv2009.1
+ Revision: 295260
- update to new version 4.3

* Tue Jun 17 2008 Guillaume Rousse <guillomovitch@mandriva.org> 4.2-2mdv2009.0
+ Revision: 223439
- add missing js directory (fix #41530)

* Fri May 30 2008 Guillaume Rousse <guillomovitch@mandriva.org> 4.2-1mdv2009.0
+ Revision: 213375
- new version
  drop patch0
  don't recompress sources

* Wed Jan 16 2008 Guillaume Rousse <guillomovitch@mandriva.org> 4.1.6-1mdv2008.1
+ Revision: 153784
- update to new version 4.1.6
- don't duplicate spec-helper encoding fix

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Wed Dec 19 2007 Guillaume Rousse <guillomovitch@mandriva.org> 4.1.5-1mdv2008.1
+ Revision: 133739
- update to new version 4.1.5

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Thu Aug 02 2007 Funda Wang <fwang@mandriva.org> 4.1.4-1mdv2008.0
+ Revision: 58112
- New version 4.1.4


* Mon Sep 04 2006 Andreas Hasenack <andreas@mandriva.com>
+ 2006-09-04 15:33:52 (59799)
- fixed registry file

* Mon Sep 04 2006 Andreas Hasenack <andreas@mandriva.com>
+ 2006-09-04 15:26:50 (59798)
- Import horde-imp

* Fri Aug 25 2006 Guillaume Rousse <guillomovitch@mandriva.org> 4.1.3-1mdv2007.0
- New version 4.1.3

* Mon Jun 26 2006 Guillaume Rousse <guillomovitch@mandriva.org> 4.1.2-1mdv2007.0
- New version 4.1.2
- decompress patch
- use herein document for horde configuration

* Tue Mar 07 2006 Guillaume Rousse <guillomovitch@mandriva.org> 4.1-1mdk
- new version

* Wed Jan 11 2006 Guillaume Rousse <guillomovitch@mandriva.org> 4.0.4-2mdk
- fix automatic dependencies

* Tue Dec 27 2005 Guillaume Rousse <guillomovitch@mandriva.org> 4.0.4-1mdk
- New release 4.0.4
- %%mkrel

* Thu Jun 30 2005 Guillaume Rousse <guillomovitch@mandriva.org> 4.0.3-2mdk 
- better fix encoding
- fix requires

* Sat Apr 16 2005 Guillaume Rousse <guillomovitch@mandrake.org> 4.0.3-1mdk
- New release 4.0.3

* Fri Feb 18 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 4.0.1-4mdk
- spec file cleanups, remove the ADVX-build stuff
- strip away annoying ^M

* Thu Jan 27 2005 Guillaume Rousse <guillomovitch@mandrake.org> 4.0.1-3mdk 
- no automatic config generation, incorrect default values
- horde isn't a prereq
- spec cleanup

* Mon Jan 17 2005 Guillaume Rousse <guillomovitch@mandrake.org> 4.0.1-2mdk 
- fix inclusion path
- fix configuration perms
- generate configuration at postinstall
- horde and rpm-helper are now a prereq

* Fri Jan 14 2005 Guillaume Rousse <guillomovitch@mandrake.org> 4.0.1-1mdk 
- new version
- top-level is now /var/www/horde/imp
- config is now in /etc/horde/imp
- other non-accessible files are now in /usr/share/horde/imp
- drop safemode build
- drop old obsoletes
- drop all patches
- no more apache configuration
- rpmbuildupdate aware
- spec cleanup

* Tue Sep 14 2004 Guillaume Rousse <guillomovitch@mandrake.org> 3.2.5-3mdk 
- remove post-installation configuration: assuming a local mail server is used is wrong

* Mon Aug 16 2004 Pascal Cavy <pascal@vmfacility.fr> 3.2.5-2mdk
- fix typo in %%post #10815

* Wed Aug 04 2004 Guillaume Rousse <guillomovitch@mandrake.org> 3.2.5-1mdk 
- new version

* Sun Jul 18 2004 Guillaume Rousse <guillomovitch@mandrake.org> 3.2.4-2mdk 
- apache config file in /etc/httpd/webapps.d

* Sat Jun 05 2004 Guillaume Rousse <guillomovitch@mandrake.org> 3.2.4-1mdk 
- new version
- rpmbuildupdate aware

* Sat May 01 2004 Guillaume Rousse <guillomovitch@mandrake.org> 3.2.3-2mdk
- renamed to horde-imp
- pluggable horde configuration
- standard perms for /etc/httpd/conf.d/%%{order}_horde-imp.conf
- don't provide useless ADVXpackage virtual package
- remove redundant requires, as horde already requires them

* Mon Apr 05 2004 Guillaume Rousse <guillomovitch@mandrake.org> 3.2.3-1mdk
- new version

* Sat Dec 20 2003 Guillaume Rousse <guillomovitch@mandrake.org> 3.2.2-3mdk
- untagged localisation files
- no more .htaccess files, use /etc/httpd/conf.d/%%{order}_imp.conf instead
- scripts now in  /usr/share/{name}

* Tue Sep 09 2003 Guillaume Rousse <guillomovitch@linux-mandrake.com> 3.2.2-2mdk
- changed name to imp, old version doesn't exist anymore
- requires horde, not horde2
- standard perms and ownership for config files, access is already denied

* Mon Sep 08 2003 Guillaume Rousse <guillomovitch@linux-mandrake.com> 3.2.2-1mdk
- 3.2.2
- speac cleanup
- remove useless files from webroot (.dist, doc files, .po)
- properly tag localisation files
- drop apache1 integration
- drop ugly configuration scripts, perl rulez
- fixed URL
- removed implicit dependencies

