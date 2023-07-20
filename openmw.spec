Summary:	A reimplementation of The Elder Scrolls III: Morrowind
Name:		openmw
Version:	0.47.0
Release:	5
Group:		Games/Adventure
License:	GPLv3+
Url:		https://openmw.org
Source0:	https://github.com/OpenMW/openmw/archive/%{version}/%{name}-%{name}-%{version}.tar.gz
Source1:	%{name}.rpmlintrc
#Patch0:		fix_include.patch
Patch1:		openmw-sigaltstack.patch
Patch2:		openmw-0.47.0-gcc12.patch
BuildRequires:	cmake
BuildRequires:	ogre
BuildRequires:	boost-devel
BuildRequires:	ffmpeg-devel
BuildRequires:	qt5-devel
BuildRequires:	pkgconfig(bullet)
BuildRequires:	pkgconfig(openscenegraph)
BuildRequires:	pkgconfig(openscenegraph-osg)
BuildRequires:	pkgconfig(liblz4)
BuildRequires:	pkgconfig(libmpg123)
BuildRequires:	pkgconfig(libunshield)
BuildRequires:	pkgconfig(MYGUI)
BuildRequires:	pkgconfig(OGRE)
BuildRequires:	pkgconfig(OIS)
BuildRequires:	pkgconfig(openal)
BuildRequires:	pkgconfig(sdl2)
BuildRequires:	pkgconfig(sndfile)
BuildRequires:	pkgconfig(uuid)
BuildRequires:	pkgconfig(xt)
BuildRequires:	tinyxml-devel
Requires:	ogre
Requires:	openscenegraph-plugins

%description
OpenMW is an engine for 2002's game The Elder Scrolls 3: Morrowind.
It aims to be a fully playable (and improved!), open source
implementation of the game's engine and functionality.

You will still need the original game data to play OpenMW.

%prep
%setup -qn %{name}-%{name}-%{version}
%autopatch -p1

# Remove bundled tinyxml files
rm -f extern/oics/tiny*.
# We don't install license files
sed -e '/LICDIR/d' -i CMakeLists.txt
# Use the system tinyxml headers
sed -e 's/"tinyxml.h"/<tinyxml.h>/g' \
	-e 's/"tinystr.h"/<tinystr.h>/g' \
	-i extern/oics/ICSPrerequisites.h


# Use bundled version of bullet (use_system_bulett=off), because OpenMW 0.46/0.47 require bullet compiled with double precision
# while OMV version was compiled as single precision. Double cause huge performance hit for all stuff that use bullet.
# That's why we use here bundled version of bullet with double precision to avoid droping performance for system bullet and rest app that depend on it.

%build
%cmake  -DOGRE_PLUGIN_DIR=%{_libdir}/OGRE \
	-DUSE_SYSTEM_TINYXML=ON \
	-DOPENMW_USE_SYSTEM_BULLET=OFF \
	-DBUILD_UNITTESTS=OFF \
	-DDESIRED_QT_VERSION=5 \
	-DMORROWIND_DATA_FILES=%{_datadir}/games/morrowind

%make_build

%install
%make_install -C build

%files
%{_sysconfdir}/%{name}/
%{_bindir}/*
%{_datadir}/metainfo/openmw.appdata.xml
%{_gamesdatadir}/%{name}/
%{_datadir}/applications/*.desktop
%{_datadir}/pixmaps/%{name}.png
%{_datadir}/pixmaps/openmw-cs.png
