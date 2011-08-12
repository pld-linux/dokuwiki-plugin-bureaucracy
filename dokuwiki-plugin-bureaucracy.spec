%define		plugin		bureaucracy
%define		php_min_version 5.1.2
%include	/usr/lib/rpm/macros.php
Summary:	Easily create HTML forms and collect the data via email or use it to create pages
Summary(pl.UTF-8):	Wtyczka bureaucracy dla DokuWiki
Name:		dokuwiki-plugin-%{plugin}
Version:	20110525
Release:	2
License:	GPL v2
Group:		Applications/WWW
Source0:	http://github.com/splitbrain/dokuwiki-plugin-%{plugin}/tarball/master#/%{plugin}.tgz
# Source0-md5:	042ceae7e1aa8b12e3a93e568846f326
URL:		http://www.dokuwiki.org/plugin:bureaucracy
BuildRequires:	rpm-php-pearprov >= 4.4.2-11
BuildRequires:	rpmbuild(macros) >= 1.520
Requires:	dokuwiki >= 20090214
Requires:	php-common >= 4:%{php_min_version}
Requires:	php-pcre
Requires:	php-spl
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
%{plugindir}/script
%{plugindir}/actions
%{plugindir}/fields
