%define gcj_support     1
%define base_name       modeler
%define short_name      commons-%{base_name}
%define section         free
%define gcj_support     1

Name:           jakarta-%{short_name}
Version:        2.0
Release:        1.5.7
Epoch:          0
Summary:        Jakarta Commons Modeler
License:        Apache License
Group:          Development/Java
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
cp -a dist/%{short_name}.jar %{buildroot}%{_javadir}/%{name}-%{version}.jar
(cd %{buildroot}%{_javadir} && for jar in *-%{version}*; do %{__ln_s} ${jar} `echo $jar| %{__sed}  "s|jakarta-||g"`; done)
(cd %{buildroot}%{_javadir} && for jar in *-%{version}*; do %{__ln_s} ${jar} `echo $jar| %{__sed}  "s|-%{version}||g"`; done)
# javadoc
%{__mkdir_p} %{buildroot}%{_javadocdir}/%{name}-%{version}
cp -a dist/docs/* %{buildroot}%{_javadocdir}/%{name}-%{version}
(cd %{buildroot}%{_javadocdir} && %{__ln_s} %{name}-%{version} %{name})

%{__perl} -pi -e 's/\r$//g' LICENSE.txt NOTICE.txt RELEASE-NOTES.txt

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
%{_libdir}/gcj/%{name}
%endif

%files javadoc
%defattr(0644,root,root,0755)
%dir %{_javadocdir}/%{name}-%{version}
%{_javadocdir}/%{name}-%{version}/*
%ghost %dir %{_javadocdir}/%{name}


%changelog
* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 0:2.0-1.5.5mdv2011.0
+ Revision: 606059
- rebuild

* Wed Mar 17 2010 Oden Eriksson <oeriksson@mandriva.com> 0:2.0-1.5.4mdv2010.1
+ Revision: 522991
- rebuilt for 2010.1

* Wed Sep 02 2009 Christophe Fergeau <cfergeau@mandriva.com> 0:2.0-1.5.3mdv2010.0
+ Revision: 425441
- rebuild

* Sat Mar 07 2009 Antoine Ginies <aginies@mandriva.com> 0:2.0-1.5.2mdv2009.1
+ Revision: 351289
- rebuild

* Tue Mar 04 2008 Alexander Kurtakov <akurtakov@mandriva.org> 0:2.0-1.5.1mdv2008.1
+ Revision: 179080
- BR java-gcj-compat-devel

  + Oden Eriksson <oeriksson@mandriva.com>
    - rebuild

  + Thierry Vignaud <tv@mandriva.org>
    - fix no-buildroot-tag
    - kill re-definition of %%buildroot on Pixel's request

  + Anssi Hannula <anssi@mandriva.org>
    - buildrequires java-rpmbuild

* Sat Sep 15 2007 Anssi Hannula <anssi@mandriva.org> 0:2.0-1.3mdv2008.0
+ Revision: 87414
- rebuild to filter out autorequires of GCJ AOT objects
- remove unnecessary Requires(post) on java-gcj-compat

* Wed Jul 18 2007 Anssi Hannula <anssi@mandriva.org> 0:2.0-1.2mdv2008.0
+ Revision: 53183
- use xml-commons-jaxp-1.3-apis explicitely instead of the generic
  xml-commons-apis which is provided by multiple packages (see bug #31473)


* Fri Mar 09 2007 David Walluck <walluck@mandriva.org> 2.0-1.1mdv2007.1
+ Revision: 140220
- 2.0
- Import jakarta-commons-modeler

* Sat Jul 22 2006 David Walluck <walluck@mandriva.org> 0:1.1-7.1mdv2007.0
- bump release

* Sat Jun 03 2006 David Walluck <walluck@mandriva.org> 0:1.1-4.3mdv2007.0
- rebuild for libgcj.so.7

* Fri Nov 11 2005 David Walluck <walluck@mandriva.org> 0:1.1-4.2mdk
- aot compile

* Fri May 20 2005 David Walluck <walluck@mandriva.org> 0:1.1-4.1mdk
- release

* Thu Feb 24 2005 David Walluck <david@jpackage.org> 0:1.1-4jpp
- add missing epochs to dependencies
- add non-versioned javadoc symlink
- fix file permissions

* Mon Aug 23 2004 Randy Watler <rwatler at finali.com> - 0:1.1-3jpp
- Rebuild with ant-1.6.2

