%define		plugin	file-upload
Summary:	File Upload library for jQuery
Name:		jquery-%{plugin}
Version:	6.7
Release:	1
License:	MIT
Group:		Applications/WWW
Source0:	https://github.com/blueimp/jQuery-File-Upload/tarball/master/%{plugin}-%{version}.tgz
# Source0-md5:	1446c835a9ff3f7a41c1d9ca3e91c2e9
URL:		https://github.com/blueimp/jQuery-File-Upload/
BuildRequires:	closure-compiler
BuildRequires:	yuicompressor
BuildRequires:	js
BuildRequires:	rpmbuild(macros) > 1.268
#Requires:	blueimp-canvas-to-blob >=1.0.1
#Requires:	blueimp-load-image >=1.1.4
#Requires:	blueimp-tmpl >=2.1.0
Requires:	jquery >= 1.6
#Requires:	jquery-ui >= 1.8
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_appdir	%{_datadir}/jquery/%{plugin}

%description
File Upload widget with multiple file selection, drag&drop support,
progress bars and preview images for jQuery. Supports cross-domain,
chunked and resumable file uploads and client-side image resizing.
Works with any server-side platform (PHP, Python, Ruby on Rails, Java,
Node.js, Go etc.) that supports standard HTML form file uploads.

%prep
%setup -qc
mv *-jQuery-File-Upload-*/* .

%build
install -d build
# compress .js
for js in $(find js -name '*.js'); do
	out=build/$js
	install -d ${out%/*}
	%if 0%{!?debug:1}
	closure-compiler --js $js --charset UTF-8 --js_output_file $out
	js -C -f $out
	%else
	cp -p $js $out
	%endif
done

# pack .css
for css in $(find css -name '*.css'); do
	out=build/$css
	install -d ${out%/*}
%if 0%{!?debug:1}
	yuicompressor --charset UTF-8 $css -o $out
%else
	cp -a $css $out
%endif
done

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_appdir}
cp -a build/* $RPM_BUILD_ROOT%{_appdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md
%{_appdir}
