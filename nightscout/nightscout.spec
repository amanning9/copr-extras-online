%global forgeurl https://github.com/nightscout/cgm-remote-monitor
Version: 14.2.2
%global tag %version

%forgemeta

Name:           nightscout
Release:        1%{?dist}
Summary:        CGM in the cloud.

License:        AGPL
URL:            %forgeurl
Source0:        %forgesource
Source1:        nightscout.service

BuildRequires:  nodejs-devel
BuildRequires:  npm
BuildRequires:  systemd-rpm-macros

Requires:       nodejs

%global debug_package %{nil}

%description
Nightscout CGM in the cloud.

%post
%systemd_post nightscout.service
if [ "$1" = 1 ]; then
    pushd %{nodejs_sitelib}/%{name}
    node bin/generateRandomString.js > %{_sysconfdir}/nightscout/randomString
    popd
fi

%preun
%systemd_preun nightscout.service

%postun
%systemd_postun_with_restart nightscout.service

%prep
%forgesetup

%build
npm install --no-audit --no-fund --omit=dev
rm tmp/randomString
ln -s %{_sysconfdir}/nightscout/randomString tmp/randomString
chmod -R -x+X *

%install
mkdir -p %{buildroot}%{nodejs_sitelib}/%{name}
cp -pr \
    package.json \
    lib \
    server.js \
    bundle \
    translations \
    views \
    bin \
    static \
    tmp \
    %{buildroot}%{nodejs_sitelib}/%{name}
cp -pr node_modules %{buildroot}%{nodejs_sitelib}/%{name}

install -m 644 -D docs/example-template.env %{buildroot}%{_sysconfdir}/nightscout/nightscout-environ
install -m 644 -D %{SOURCE1} %{buildroot}%{_unitdir}/nightscout.service

%files
%license LICENSE
%doc README.md
%{nodejs_sitelib}/%{name}
%{_unitdir}/nightscout.service
%config(noreplace) %{_sysconfdir}/nightscout

%changelog
* Fri Feb 26 12:10:49 GMT 2021 Alex Manning <git@alex-m.co.uk>
-
