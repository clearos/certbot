%global oldpkg letsencrypt

Name:           certbot
Version:        0.8.0
Release:        1%{?dist}
Summary:        A free, automated certificate authority client

License:        ASL 2.0
URL:            https://pypi.python.org/pypi/certbot
Source0:        https://files.pythonhosted.org/packages/source/c/%{name}/%{name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python2-devel

Requires: python2-certbot = %{version}-%{release}
Obsoletes: %{oldpkg} < 0.6.0
Provides: %{oldpkg} = %{version}-%{release}

# Required for documentation
BuildRequires: python-sphinx
BuildRequires: python-sphinx_rtd_theme
BuildRequires: python-repoze-sphinx-autointerface
BuildRequires: python-sphinxcontrib-programoutput


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

%prep
%autosetup -n %{name}-%{version}


%build
# We are using certbot and not supporting certbot-auto
sed -i 's/letsencrypt-auto/certbot/g' certbot/cli.py
%py2_build

# build documentation
%{__python2} setup.py install --user
make -C docs  man PATH=${HOME}/.local/bin:$PATH

%install
%py2_install
# Add compatibility symlink as requested by upstream conference call
ln -sf /usr/bin/certbot %{buildroot}/usr/bin/%{oldpkg}
# Put the man pages in place
install -pD -t %{buildroot}%{_mandir}/man1 docs/_build/man/*1*


%check
%{__python2} setup.py test

%files
%license LICENSE.txt
%doc README.rst CHANGES.rst CONTRIBUTING.md
%{_bindir}/certbot
%{_bindir}/%{oldpkg}
%doc %attr(0644,root,root) %{_mandir}/man1/%{name}*
# project uses old letsencrypt dir for compatibility
%ghost %dir %{_sysconfdir}/%{oldpkg}
%ghost %dir %{_sharedstatedir}/%{oldpkg}

%files -n python2-certbot
%license LICENSE.txt
%{python2_sitelib}/%{name}
%{python2_sitelib}/%{name}-%{version}*.egg-info

%changelog
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
