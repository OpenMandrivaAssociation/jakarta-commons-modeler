%define gcj_support     1
%define base_name       modeler
%define short_name      commons-%{base_name}
%define section         free
%define gcj_support     1

Name:           jakarta-%{short_name}
Version:        2.0
Release:        %mkrel 1.5.6
Epoch:          0
Summary:        Jakarta Commons Modeler
License:        Apache License
Group:          Development/Java
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
#Vendor:        JPackage Project
#Distribution:  JPackage
Source0:        http://www.apache.org/dist/jakarta/commons/modeler/source/commons-modeler-2.0-src.tar.gz
Url:            http://jakarta.apache.org/commons/%{base_name}/
BuildRequires:  java-rpmbuild
BuildRequires:  ant
BuildRequires:  jaxp_parser_impl
BuildRequires:  xml-commons-jaxp-1.3-apis
BuildRequires:  jaxp_transform_impl
# XXX: jmxri doesn't work because mx4j requires mx4j.util.Utils (mx4j-tools)
BuildRequires:  mx4j
BuildRequires:  junit >= 0:3.7
BuildRequires:  jakarta-commons-beanutils >= 0:1.3
BuildRequires:  jakarta-commons-collections >= 0:2.0
BuildRequires:  jakarta-commons-digester >= 0:1.2
BuildRequires:  jakarta-commons-logging >= 0:1.0
Requires:       jaxp_parser_impl
Requires:       xml-commons-jaxp-1.3-apis
Requires:       jaxp_transform_impl
Requires:       mx4j
Requires:       jakarta-commons-beanutils >= 0:1.3
Requires:       jakarta-commons-collections >= 0:2.0
Requires:       jakarta-commons-digester >= 0:1.2
Requires:       jakarta-commons-logging >= 0:1.0
%if %{gcj_support}
BuildRequires:  java-gcj-compat-devel
%else
BuildArch:      noarch
BuildRequires:  java-devel
%endif
Provides:        %{short_name}
Obsoletes:       %{short_name}

%description
The Modeler project shall create and maintain a set of Java
classes to provide the facilities described in the preceeding section, plus
unit tests and small examples of using these facilities to instrument
Java classes with Model MBean support.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java

%description javadoc
Javadoc for %{name}.

%prep
%setup -q -n %{short_name}-%{version}-src

%build
export CLASSPATH=$(build-classpath xml-commons-jaxp-1.3-apis jaxp_parser_impl jaxp_transform_impl mx4j junit commons-beanutils commons-collections commons-digester commons-logging junit)
%{ant} dist
%{ant} -Dbuild.sysclasspath=first test

%install
%{__rm} -rf %{buildroot}

# jars
%{__mkdir_p} %{buildroot}%{_javadir}
%{__cp} -a dist/%{short_name}.jar %{buildroot}%{_javadir}/%{name}-%{version}.jar
(cd %{buildroot}%{_javadir} && for jar in *-%{version}*; do %{__ln_s} ${jar} `echo $jar| %{__sed}  "s|jakarta-||g"`; done)
(cd %{buildroot}%{_javadir} && for jar in *-%{version}*; do %{__ln_s} ${jar} `echo $jar| %{__sed}  "s|-%{version}||g"`; done)
# javadoc
%{__mkdir_p} %{buildroot}%{_javadocdir}/%{name}-%{version}
%{__cp} -a dist/docs/* %{buildroot}%{_javadocdir}/%{name}-%{version}
(cd %{buildroot}%{_javadocdir} && %{__ln_s} %{name}-%{version} %{name})

%{__perl} -pi -e 's/\r$//g' LICENSE.txt NOTICE.txt RELEASE-NOTES.txt

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
%{__rm} -rf %{buildroot}

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%post javadoc
%{__rm} -f %{_javadocdir}/%{name}
%{__ln_s} %{name}-%{version} %{_javadocdir}/%{name}

%postun javadoc
if [ $1 -eq 0 ]; then
  %{__rm} -f %{_javadocdir}/%{name}
fi

%files
%defattr(0644,root,root,0755)
%doc LICENSE.txt NOTICE.txt RELEASE-NOTES.txt
%{_javadir}/*
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}
%endif

%files javadoc
%defattr(0644,root,root,0755)
%dir %{_javadocdir}/%{name}-%{version}
%{_javadocdir}/%{name}-%{version}/*
%ghost %dir %{_javadocdir}/%{name}


