%global forgeurl https://github.com/go-gitea/gitea
Version: 1.15.6

%forgemeta

Name:           gitea
Release:        1%{?dist}
Summary:        Gitea

License:        MIT
URL:            %forgeurl
Source0:        %forgesource
Source1:        gitea.service

BuildRequires:  golang
BuildRequires:  nodejs
BuildRequires:  npm
BuildRequires:  systemd-rpm-macros
BuildRequires:  gcc

%description
Gitea

%global debug_package %{nil}

%post
%systemd_post gitea.service

%preun
%systemd_preun gitea.service

%postun
%systemd_postun_with_restart gitea.service

%prep
%autosetup

%build
%global ldflags -X \"code.gitea.io/gitea/modules/setting.CustomPath=/etc/gitea/\" -X \"code.gitea.io/gitea/modules/setting.AppWorkPath=/var/lib/gitea\" -X \"code.gitea.io/gitea/modules/setting.StaticRootPath=/var/lib/gitea/static\" -X \"code.gitea.io/gitea/modules/setting.PIDFile=/run/gitea/gitea.pid\"
TAGS="bindata" LDFLAGS="%{ldflags}" %{__make} build

%install
install -m 0755 -D gitea %{buildroot}%{_bindir}/gitea

install -D %{SOURCE1} %{buildroot}%{_unitdir}/gitea.service

mkdir -p %{buildroot}%{_sysconfdir}/gitea
mkdir -p %{buildroot}%{_libdir}/gitea
mkdir -p %{buildroot}%{_rundir}/gitea

%files
%license LICENSE
%doc README.md

%config(noreplace) %{_sysconfdir}/gitea
%{_rundir}/gitea
%{_libdir}/gitea
/usr/bin/gitea
%{_unitdir}/gitea.service

%changelog
* Wed Feb 24 18:41:47 GMT 2021 Alex Manning <git@alex-m.co.uk>
-
