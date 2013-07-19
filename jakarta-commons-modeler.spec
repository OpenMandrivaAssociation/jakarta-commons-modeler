%define gcj_support	1
%define base_name	modeler
%define short_name	commons-%{base_name}
%define section		free
%define gcj_support	1

Summary:	Jakarta Commons Modeler
Name:		jakarta-%{short_name}
Version:	2.0.1
Release:	1
License:	Apache License
Group:		Development/Java
Url:		http://jakarta.apache.org/commons/%{base_name}/
Source0:	http://www.apache.org/dist/jakarta/commons/modeler/source/commons-modeler-2.0.1-src.tar.gz
%if !%{gcj_support}
BuildArch:	noarch
BuildRequires:	java-devel
%else
BuildRequires:	java-gcj-compat-devel
BuildRequires:	ant
BuildRequires:	jakarta-commons-beanutils >= 0:1.3
BuildRequires:	jakarta-commons-collections >= 0:2.0
BuildRequires:	jakarta-commons-digester >= 0:1.2
BuildRequires:	jakarta-commons-logging >= 0:1.0
BuildRequires:	java-rpmbuild
BuildRequires:	jaxp_parser_impl
BuildRequires:	jaxp_transform_impl
BuildRequires:	junit >= 0:3.7
# XXX:	jmxri doesn't work because mx4j requires mx4j.util.Utils (mx4j-tools)
BuildRequires:	mx4j
BuildRequires:	xml-commons-jaxp-1.3-apis
Requires:	jakarta-commons-beanutils >= 0:1.3
Requires:	jakarta-commons-collections >= 0:2.0
Requires:	jakarta-commons-digester >= 0:1.2
Requires:	jakarta-commons-logging >= 0:1.0
Requires:	jaxp_parser_impl
Requires:	jaxp_transform_impl
Requires:	mx4j
Requires:	xml-commons-jaxp-1.3-apis
%endif
Provides:	%{short_name}

%description
The Modeler project shall create and maintain a set of Java
classes to provide the facilities described in the preceeding section, plus
unit tests and small examples of using these facilities to instrument
Java classes with Model MBean support.

%package javadoc
Summary:	Javadoc for %{name}
Group:		Development/Java

%description javadoc
Javadoc for %{name}.

%prep
%setup -qn %{short_name}-%{version}-src

%build
export CLASSPATH=$(build-classpath xml-commons-jaxp-1.3-apis jaxp_parser_impl jaxp_transform_impl mx4j junit commons-beanutils commons-collections commons-digester commons-logging junit)
%{ant} dist
%{ant} -Dbuild.sysclasspath=first test

%install
# jars
mkdir -p %{buildroot}%{_javadir}
cp -a dist/%{short_name}.jar %{buildroot}%{_javadir}/%{name}-%{version}.jar
(cd %{buildroot}%{_javadir} && for jar in *-%{version}*; do ln -s ${jar} `echo $jar| %{__sed}  "s|jakarta-||g"`; done)
(cd %{buildroot}%{_javadir} && for jar in *-%{version}*; do ln -s ${jar} `echo $jar| %{__sed}  "s|-%{version}||g"`; done)
# javadoc
mkdir -p %{buildroot}%{_javadocdir}/%{name}-%{version}
cp -a dist/docs/* %{buildroot}%{_javadocdir}/%{name}-%{version}
(cd %{buildroot}%{_javadocdir} && ln -s %{name}-%{version} %{name})

sed -i -e 's/\r$//g' LICENSE.txt NOTICE.txt RELEASE-NOTES.txt

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%post javadoc
rm -f %{_javadocdir}/%{name}
ln -s %{name}-%{version} %{_javadocdir}/%{name}

%postun javadoc
if [ $1 -eq 0 ]; then
  %{__rm} -f %{_javadocdir}/%{name}
fi

%files
%doc LICENSE.txt NOTICE.txt RELEASE-NOTES.txt
%{_javadir}/*
%if %{gcj_support}
%{_libdir}/gcj/%{name}
%endif

%files javadoc
%dir %{_javadocdir}/%{name}-%{version}
%{_javadocdir}/%{name}-%{version}/*
%ghost %dir %{_javadocdir}/%{name}


