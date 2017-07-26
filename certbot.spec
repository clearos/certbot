%global oldpkg letsencrypt

# On fedora use python3 for certbot
%if 0%{?fedora}
%bcond_without python3
%else
%bcond_with python3
%endif


Name:           certbot
Version:        0.14.1
Release:        4%{?dist}
Summary:        A free, automated certificate authority client

License:        ASL 2.0
URL:            https://pypi.python.org/pypi/certbot
Source0:        https://files.pythonhosted.org/packages/source/c/%{name}/%{name}-%{version}.tar.gz

Source10:       certbot-renew-systemd.service
Source11:       certbot-renew-systemd.timer
Source12:       certbot-sysconfig-certbot
Source13:       certbot-README.fedora

%if 0%{?rhel}
Patch0:         allow-old-setuptools.patch
%endif

BuildArch:      noarch

%if %{with python3}
BuildRequires:  python3-devel
BuildRequires:  python3-future
%endif

BuildRequires:  python2-devel
BuildRequires:  python2-future

# For the systemd macros
%{?systemd_requires}
BuildRequires:  systemd

# Need to label the httpd rw stuff correctly until base selinux policy updated
Requires(post):   %{_sbindir}/semanage
Requires(postun): %{_sbindir}/semanage

# On F26+ use python3
%if 0%{?fedora} >= 26
Requires: python3-certbot = %{version}-%{release}
%else
Requires: python2-certbot = %{version}-%{release}
%endif

Obsoletes: %{oldpkg} < 0.6.0
Provides: %{oldpkg} = %{version}-%{release}

# Required for documentation
BuildRequires: python-sphinx
BuildRequires: python-sphinx_rtd_theme
BuildRequires: python-repoze-sphinx-autointerface

#Require for testing
BuildRequires: python-nose-xcover
BuildRequires: python-pep8
BuildRequires: python-tox
BuildRequires: python-mock
BuildRequires: python-configargparse >= 0.10.0
BuildRequires: python-zope-interface
BuildRequires: python-zope-component
BuildRequires: python-requests
BuildRequires: python2-dialog >= 3.3.0
BuildRequires: python-psutil >= 2.1.0
BuildRequires: python-parsedatetime
BuildRequires: python-configobj
BuildRequires: python2-configargparse >= 0.10.0
BuildRequires: python2-acme = %{version}

%if %{with python3}
#Require for testing
BuildRequires: python3-nose-xcover
BuildRequires: python3-pep8
BuildRequires: python3-tox
BuildRequires: python3-mock
BuildRequires: python3-configargparse >= 0.10.0
BuildRequires: python3-zope-interface
BuildRequires: python3-zope-component
BuildRequires: python3-requests
BuildRequires: python3-dialog >= 3.3.0
BuildRequires: python3-psutil >= 2.1.0
BuildRequires: python3-parsedatetime
BuildRequires: python3-configobj
BuildRequires: python3-configargparse >= 0.10.0
BuildRequires: python3-acme = %{version}
%endif

%description
certbot is a free, automated certificate authority that aims
to lower the barriers to entry for encrypting all HTTP traffic on the internet.

%package -n python2-certbot
Requires:   python2-configargparse >= 0.10.0
Requires:   python2-dialog >= 3.3.0
Requires:   python-parsedatetime
Requires:   python-mock
Requires:   python-zope-interface
Requires:   python-zope-component
Requires:   python-psutil >= 2.1.0
Requires:   python-configobj
Requires:   python2-future
Requires:   python2-acme = %{version}
Obsoletes:  python2-%{oldpkg} <  0.6.0
Provides:   python2-%{oldpkg} = %{version}-%{release}
Obsoletes:  python-%{oldpkg} <  0.6.0
Provides:   python-%{oldpkg} = %{version}-%{release}
#Recommends: certbot-doc
Summary:    Python 2 libraries used by certbot
%{?python_provide:%python_provide python2-certbot}

%description -n python2-certbot
The python2 libraries to interface with certbot


%if %{with python3}
%package -n python3-certbot
Requires:   python3-configargparse >= 0.10.0
Requires:   python3-dialog >= 3.3.0
Requires:   python3-parsedatetime
Requires:   python3-mock
Requires:   python3-zope-interface
Requires:   python3-zope-component
Requires:   python3-psutil >= 2.1.0
Requires:   python3-future
Requires:   python3-configobj
Requires:   python3-acme = %{version}
Summary:    Python 3 libraries used by certbot
%{?python_provide:%python_provide python3-certbot}

%description -n python3-certbot
The python3 libraries to interface with certbot

%endif

%prep
%autosetup -n %{name}-%{version} -p1


%build
%py2_build
%if %{with python3}
%py3_build
%endif

# build documentation
# %{__python2} setup.py install --user
# make -C docs  man PATH=${HOME}/.local/bin:$PATH

%install
%py2_install
mv %{buildroot}%{_bindir}/certbot{,-2}
%if %{with python3}
%py3_install
mv %{buildroot}%{_bindir}/certbot{,-3}
%endif
# Add compatibility symlink as requested by upstream conference call
ln -sf /usr/bin/certbot %{buildroot}/usr/bin/%{oldpkg}
# Put the man pages in place
# install -pD -t %{buildroot}%{_mandir}/man1 docs/_build/man/*1*
# On F26+ use python3
%if 0%{?fedora} >= 26
ln -s %{_bindir}/certbot-3 %{buildroot}%{_bindir}/certbot
%else
ln -s %{_bindir}/certbot-2 %{buildroot}%{_bindir}/certbot
%endif
install -Dm 0644 %{SOURCE10} %{buildroot}%{_unitdir}/certbot-renew.service
install -Dm 0644 %{SOURCE11} %{buildroot}%{_unitdir}/certbot-renew.timer
install -Dm 0644 %{SOURCE12} %{buildroot}%{_sysconfdir}/sysconfig/certbot
mv %{SOURCE13} README.fedora

%check
%{__python2} setup.py test
%if %{with python3}
%{__python3} setup.py test
%endif
# Make sure the scripts use the expected python versions
grep -q %{__python2} %{buildroot}%{_bindir}/certbot-2
%if %{with python3}
grep -q %{__python3} %{buildroot}%{_bindir}/certbot-3
%endif

# The base selinux policies don't handle the certbot directories yet so set them up manually
%post
semanage fcontext -a -t cert_t '%{_sysconfdir}/(letsencrypt|certbot)/(live|archive)(/.*)?'
restorecon -R %{_sysconfdir}/letsencrypt || :

%files
%license LICENSE.txt
%doc README.rst CHANGES.rst CONTRIBUTING.md README.fedora
%{_bindir}/certbot
%{_bindir}/%{oldpkg}
# %doc %attr(0644,root,root) %{_mandir}/man1/%{name}*
# project uses old letsencrypt dir for compatibility
%ghost %dir %{_sysconfdir}/%{oldpkg}
%ghost %dir %{_sharedstatedir}/%{oldpkg}
%config %{_sysconfdir}/sysconfig/certbot
%{_unitdir}/certbot-renew.service
%{_unitdir}/certbot-renew.timer

%files -n python2-certbot
%license LICENSE.txt
%{python2_sitelib}/%{name}
%{python2_sitelib}/%{name}-%{version}*.egg-info
%{_bindir}/certbot-2

%if %{with python3}
%files -n python3-certbot
%license LICENSE.txt
%{python3_sitelib}/%{name}
%{python3_sitelib}/%{name}-%{version}*.egg-info
%{_bindir}/certbot-3
%endif

%changelog
* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu May 18 2017 James Hogarth <james.hogarth@gmail.com> - 0.14.1-3
- Further tweaks after upstream feedback
- On F26+ use python3

* Wed May 17 2017 James Hogarth <james.hogarth@gmail.com> - 0.14.1-2
- Tweaks to the renew service bz#1444814

* Tue May 16 2017 James Hogarth <james.hogarth@gmail.com> - 0.14.1-1
- Update to 0.14.1

* Fri May 12 2017 James Hogarth <james.hogarth@gmail.com> - 0.14.0-1
- Update to 0.14.0
- Fix for bz#1444814

* Fri Apr 28 2017 James Hogarth <james.hogarth@gmail.com> - 0.13.0-2
- Incorrect target for timer

* Wed Apr 19 2017 James Hogarth <james.hogarth@gmail.com> - 0.13.0-1
* Update to 0.13.0
- Timer tweaks bz#1441846
* Tue Mar 07 2017 James Hogarth <james.hogarth@gmail.com> - 0.12.0-4
- Up the timer to daily at the request of upstream
* Mon Mar 06 2017 James Hogarth <james.hogarth@gmail.com> - 0.12.0-3
- Label the certificates generated by certbot with correct selinux context
- Include optional timer for automated renewal
* Mon Mar 06 2017 James Hogarth <james.hogarth@gmail.com> - 0.12.0-2
- upstream request not to use py3 yet so switch to py2 for default
- include a py3 option for testing
* Fri Mar 03 2017 James Hogarth <james.hogarth@gmail.com> - 0.12.0-1
- update to 0.12.0
* Fri Feb 17 2017 James Hogarth <james.hogarth@gmail.com> - 0.11.1-4
- change to python3 now certbot supports it
* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.11.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild
* Sat Feb 04 2017 James Hogarth <james.hogarth@gmail.com> - 0.11.1-2
- parsedatetime needs future but doesn't declare it
* Sat Feb 04 2017 James Hogarth <james.hogarth@gmail.com> - 0.11.1-1
- Upgrade to 0.11.1
* Thu Jan 05 2017 Adam Williamson <awilliam@redhat.com> - 0.9.3-2
- Doc generation no longer needs sphinxcontrib-programoutput
- Work around Python dep generator dependency problem (#1410631)
* Fri Oct 14 2016 Nick Bebout <nb@fedoraproject.org> - 0.9.3-1
- Update to 0.9.3
* Thu Oct 13 2016 Nick Bebout <nb@fedoraproject.org> - 0.9.2-1
- Update to 0.9.2
* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-3
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages
* Wed Jul 06 2016 Robert Buchholz <rbu@fedoraproject.org> - 0.8.1-2
- Remove sed-replace that changes help output and code behavior, closes #1348391
* Wed Jun 15 2016 Nick Bebout <nb@fedoraproject.org> - 0.8.1-1
- Update to 0.8.1
* Fri Jun 03 2016 james <james.hogarth@gmail.com> - 0.8.0-1
- update to 0.8.0 release
* Tue May 31 2016 James Hogarth <james.hogarth@gmail.com> - 0.7.0-1
- Update to 0.7.0
* Thu May 12 2016 Nick Bebout <nb@fedoraproject.org> - 0.6.0-2
- Bump release to 2 since 1.0devXXX is greater than 1
* Thu May 12 2016 Nick Bebout <nb@fedoraproject.org> - 0.6.0-1
- Update to 0.6.0
* Thu May 12 2016 James Hogarth <james.hogarth@gmail.com> - 0.6.0-1.0dev0git41f347d
- Update with compatibility symlink requested from upstream 
- Update with fixes from review
* Sun May 08 2016 James Hogarth <james.hogarth@gmail.com> - 0.6.0-0.0dev0git38d7503
- Upgrade to 0.6.0 dev snapshot
- Rename to certbot to match upstream rename
* Wed Apr 06 2016 Nick Bebout <nb@fedoraproject.org> - 0.5.0-1
- Upgrade to 0.5.0
* Sat Mar 05 2016 Robert Buchholz <rbu@fedoraproject.org> - 0.4.2-3
- Package does not require python-werkzeug anymore, upstream #2453
* Fri Mar 04 2016 Robert Buchholz <rbu@fedoraproject.org> - 0.4.2-2
- Fix build on EL7 where no newer setuptools is available
* Fri Mar 04 2016 Robert Buchholz <rbu@fedoraproject.org> - 0.4.2-1
- Upgrade to 0.4.2
* Tue Mar 1 2016 Nick Le Mouton <nick@noodles.net.nz> - 0.4.1-1
- Update to 0.4.1
* Thu Feb 11 2016 Nick Bebout <nb@fedoraproject.org> - 0.4.0-1
- Update to 0.4.0
* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild
* Thu Jan 28 2016 Nick Bebout <nb@fedoraproject.org> - 0.3.0-1
- Update to 0.3.0
* Sat Jan 23 2016 Robert Buchholz <rbu@fedoraproject.org> - 0.2.0-4
- Use acme dependency version consistently and add psutil min version
* Fri Jan 22 2016 Nick Bebout <nb@fedoraproject.org> - 0.2.0-3
- Update the configargparse version in other places
* Fri Jan 22 2016 Nick Bebout <nb@fedoraproject.org> - 0.2.0-2
- Update python-configargparse version requirement
* Thu Jan 21 2016 Nick Bebout <nb@fedoraproject.org> - 0.2.0-1
- Apache plugin support for non-Debian based systems
- Relaxed PyOpenSSL version requirements
- Resolves issues with the Apache plugin enabling redirect
- Improved error messages from the client
* Wed Dec 16 2015 Nick Bebout <nb@fedoraproject.org> - 0.1.1-2
- Fix packaging issues
* Wed Dec 16 2015 Nick Bebout <nb@fedoraproject.org> - 0.1.1-1
- fix a confusing UI path that caused some users to repeatedly renew their
- certs while experimenting with the client, in some cases hitting issuance rate limits
- numerous Apache configuration parser fixes
- avoid attempting to issue for unqualified domain names like "localhost"
- fix --webroot permission handling for non-root users
* Tue Dec 08 2015 Nick Bebout <nb@fedoraproject.org> - 0.1.0-3
- Add python-sphinx_rtd_theme build requirement
* Fri Dec 04 2015 James Hogarth <james.hogarth@gmail.com> - 0.1.0-2
- Add documentation from upstream
* Thu Dec 03 2015 James Hogarth <james.hogarth@gmail.com> - 0.1.0-1
- Update to new upstream release for the open beta
* Thu Dec 03 2015 James Hogarth <james.hogarth@gmail.com> - 0.0.0-5.dev20151123
- Add missing build requirements that slipped through
* Wed Dec 02 2015 James Hogarth <james.hogarth@gmail.com> - 0.0.0-4.dev20151123
- The python2 library should have the dependencies and not the bindir one
* Wed Dec 02 2015 James Hogarth <james.hogarth@gmail.com> - 0.0.0-3.dev20151123
- Separate out the python libraries from the application itself
- Enable python tests
* Tue Dec 01 2015 James Hogarth <james.hogarth@gmail.com> - 0.0.0-2.dev20151123
- Update spec to account for the runtime dependencies discovered
- Update spec to sit inline with current python practices
* Sun Apr 26 2015 Torrie Fischer <tdfischer@hackerbots.net> 0-1.git1d8281d.fc20
- Initial package
