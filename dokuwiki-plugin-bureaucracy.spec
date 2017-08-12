%define		subver		2017-07-27
%define		ver		%(echo %{subver} | tr -d -)
%define		plugin		bureaucracy
%define		php_min_version 5.1.2
%include	/usr/lib/rpm/macros.php
Summary:	Easily create HTML forms and collect the data via email or use it to create pages
Summary(pl.UTF-8):	Wtyczka bureaucracy dla DokuWiki
Name:		dokuwiki-plugin-%{plugin}
Version:	%{ver}
Release:	1
License:	GPL v2
Group:		Applications/WWW
Source0:	https://github.com/splitbrain/dokuwiki-plugin-%{plugin}/archive/%{subver}/%{plugin}-%{version}.tar.gz
# Source0-md5:	8eb3f12f2c2c622019cf503f9a0c0ff8
URL:		https://www.dokuwiki.org/plugin:bureaucracy
BuildRequires:	rpm-php-pearprov >= 4.4.2-11
BuildRequires:	rpmbuild(macros) >= 1.520
Requires:	dokuwiki >= 20131208
Requires:	php(core) >= %{php_min_version}
Requires:	php(pcre)
Requires:	php(spl)
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		dokuconf	/etc/webapps/dokuwiki
%define		dokudir		/usr/share/dokuwiki
%define		plugindir	%{dokudir}/lib/plugins/%{plugin}
%define		find_lang 	%{_usrlibrpm}/dokuwiki-find-lang.sh %{buildroot}

%description
The bureaucracy plugin allows you to create a HTML form right within
DokuWiki.

Input format validation is automatically handled by the plugin and
requires no coding. User input can be emailed to a preconfigured
address or used to create new pages using a template.

%prep
%setup -qc
mv *-%{plugin}-*/* .
rm -r *-%{plugin}-*
rm -r _test

%build
version=$(awk '/^date/{print $2}' plugin.info.txt)
if [ "$(echo "$version" | tr -d -)" != %{version} ]; then
	: %%{version} mismatch
	exit 1
fi

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{plugindir}
cp -a . $RPM_BUILD_ROOT%{plugindir}
%{__rm} $RPM_BUILD_ROOT%{plugindir}/README

%find_lang %{name}.lang

%clean
rm -rf $RPM_BUILD_ROOT

%post
# force js/css cache refresh
if [ -f %{dokuconf}/local.php ]; then
	touch %{dokuconf}/local.php
fi

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc README
%dir %{plugindir}
%{plugindir}/*.css
%{plugindir}/*.js
%{plugindir}/*.php
%{plugindir}/*.txt
%{plugindir}/conf
%{plugindir}/helper
%{plugindir}/interfaces
%{plugindir}/script
