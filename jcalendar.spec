%{?_javapackages_macros:%_javapackages_macros}

%define oname JCalendar
%define name %(echo %oname | tr [:upper:] [:lower:])

Summary:	A Java date chooser bean for graphically picking a date
Name:		%{name}
Version:	1.4
Release:	1
License:	LGPLv2+
Group:		Development/Java
URL:		http://toedter.com/%{name}
Source0:	http://www.toedter.com/download/%{name}-%{version}.zip
Source1:	https://repo1.maven.org/maven2/com/toedter/%{name}/%{version}/%{name}-%{version}.pom
BuildArch:	noarch

BuildRequires:	maven-local
BuildRequires:	mvn(com.jgoodies:jgoodies-looks)

%description
JCalendar is composed of several other Java beans, a JDayChooser, a
JMonthChooser and a JYearChooser. All these beans have a locale property,
provide several icons (Color 16×16, Color 32×32, Mono 16×16 and Mono 32×32)
and their own locale property editor. So they can easily be used in GUI
builders. Also part of the package is a JDateChooser, a bean composed of
an IDateEditor (for direct date editing) and a button for opening a JCalendar
for selecting the date.

%files -f .mfiles
%doc jcalendar-license.txt
%doc readme.txt
%doc doc/demo.html
%doc doc/index.html
%doc doc/license.html
%doc doc/new.html
%doc doc/style.css
%doc doc/images

#----------------------------------------------------------------------------

%package javadoc
Summary:	Javadoc for %{name}

%description javadoc
API documentation for %{name}.

%files javadoc -f .mfiles-javadoc

#----------------------------------------------------------------------------

%prep
%setup -q -c -T -b 0
# Delete all prebuild JARs and classes
find . -name "*.jar" -delete
find . -name "*.class" -delete
rm -fr bin doc/api lib/*

# pom.xml file
cp %{SOURCE1} pom.xml

# Bundle
%pom_xpath_inject "pom:project" "<packaging>bundle</packaging>" .

# Add an OSGi compilant MANIFEST.MF
%pom_add_plugin org.apache.felix:maven-bundle-plugin . "
<extensions>true</extensions>
<configuration>
	<supportedProjectTypes>
		<supportedProjectType>bundle</supportedProjectType>
		<supportedProjectType>jar</supportedProjectType>
	</supportedProjectTypes>
	<instructions>
		<Bundle-Name>\${project.artifactId}</Bundle-Name>
		<Bundle-Version>\${project.version}</Bundle-Version>
	</instructions>
</configuration>
<executions>
	<execution>
		<id>bundle-manifest</id>
		<phase>process-classes</phase>
		<goals>
			<goal>manifest</goal>
		</goals>
	</execution>
</executions>"

# Add the META-INF/INDEX.LIST (fix jar-not-indexed warning) and
# the META-INF/MANIFEST.MF to the jar archive
%pom_add_plugin :maven-jar-plugin . "
<executions>
	<execution>
		<phase>package</phase>
		<configuration>
			<archive>
				<manifestFile>\${project.build.outputDirectory}/META-INF/MANIFEST.MF</manifestFile>
				<manifest>
					<addDefaultImplementationEntries>true</addDefaultImplementationEntries>
					<addDefaultSpecificationEntries>true</addDefaultSpecificationEntries>
				</manifest>
				<index>true</index>
			</archive>
		</configuration>
		<goals>
			<goal>jar</goal>
		</goals>
	</execution>
</executions>"

# Fix the sources path
%pom_xpath_inject "pom:project/pom:build" "<sourceDirectory>src</sourceDirectory>" .

# Fix jar name
%mvn_file :%{name} %{name}-%{version} %{name}

%build
%mvn_build -- -Dproject.build.sourceEncoding=UTF-8 

%install
%mvn_install

