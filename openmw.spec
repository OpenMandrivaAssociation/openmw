#define _disable_ld_no_undefined 1
#define _disable_lto 1

Summary:	A reimplementation of The Elder Scrolls III: Morrowind
Name:		openmw
Version:	0.50.0
Release:	4
Group:		Games/Adventure
License:	GPLv3+
Url:		https://openmw.org
Source0:	https://github.com/OpenMW/openmw/archive/%{version}/%{name}-%{name}-%{version}.tar.gz
Source1:	%{name}.rpmlintrc
Source2:	https://github.com/bulletphysics/bullet3/archive/refs/tags/3.17.tar.gz

BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	ogre
BuildRequires:	boost-devel
BuildRequires:	ffmpeg-devel
BuildRequires:	qmake-qt6
BuildRequires:  cmake(Qt6)
BuildRequires:  cmake(Qt6Core)
BuildRequires:	cmake(Qt6DBus)
BuildRequires:	cmake(Qt6Gui)
BuildRequires:  cmake(Qt6Network)
BuildRequires:	cmake(Qt6Widgets)
BuildRequires:  cmake(Qt6OpenGL)
BuildRequires:  cmake(Qt6OpenGLWidgets)
BuildRequires:  cmake(Qt6Svg)
BuildRequires:	qt6-qtbase-theme-gtk3
BuildRequires:	cmake(Qt6Linguist)
BuildRequires:	pkgconfig(bullet)
BuildRequires:	pkgconfig(openscenegraph)
BuildRequires:	pkgconfig(openscenegraph-osg)
BuildRequires:	pkgconfig(liblz4)
BuildRequires:	pkgconfig(libmpg123)
BuildRequires:	pkgconfig(libunshield)
BuildRequires:	pkgconfig(luajit)
BuildRequires:	pkgconfig(MYGUI)
BuildRequires:	pkgconfig(OGRE)
BuildRequires:	pkgconfig(OIS)
BuildRequires:	pkgconfig(openal)
BuildRequires:	pkgconfig(recastnavigation)
BuildRequires:	pkgconfig(sdl2)
BuildRequires:	pkgconfig(sndfile)
BuildRequires:	pkgconfig(sqlite3)
BuildRequires:	pkgconfig(uuid)
BuildRequires:	pkgconfig(xt)
BuildRequires:	pkgconfig(yaml-cpp)
BuildRequires:	tinyxml-devel
Requires:	ogre
Requires:	openscenegraph-plugins

%patchlist
openmw-clang-21.patch

%description
OpenMW is an engine for 2002's game The Elder Scrolls 3: Morrowind.
It aims to be a fully playable (and improved!), open source
implementation of the game's engine and functionality.

You will still need the original game data to play OpenMW.

%prep
%autosetup -p1 -n %{name}-%{name}-%{version}

# Remove bundled tinyxml files
rm -f extern/oics/tiny*.
# We don't install license files
sed -e '/LICDIR/d' -i CMakeLists.txt
# Use the system tinyxml headers
sed -e 's/"tinyxml.h"/<tinyxml.h>/g' \
	-e 's/"tinystr.h"/<tinystr.h>/g' \
	-i extern/oics/ICSPrerequisites.h

# Fix for boost 1.89
sed -i -e 's/\<system\>//' -e 's/  */ /g' CMakeLists.txt
sed -i '/Boost::system/d' components/CMakeLists.txt

#find . -name "*.hpp" -o -name "*.h" -o -name "*.cpp" -o -name "*.c" |xargs sed -i -e '/include.*MyGUI/i#include <cstdint>'


# Use bundled version of bullet (use_system_bulett=off), because OpenMW 0.46/0.47 require bullet compiled with double precision
# while OMV version was compiled as single precision. Double cause huge performance hit for all stuff that use bullet.
# That's why we use here bundled version of bullet with double precision to avoid droping performance for system bullet and rest app that depend on it.
mkdir -p build/_deps/bullet-subbuild/bullet-populate-prefix/src
cp %{S:2} build/_deps/bullet-subbuild/bullet-populate-prefix/src/
# replaced with system library
#mkdir -p build/_deps/recastnavigation-subbuild/recastnavigation-populate-prefix/src
#cp %{S:3} build/_deps/recastnavigation-subbuild/recastnavigation-populate-prefix/src/

%build
export CMAKE_PREFIX_PATH=%{_libdir}/cmake/Qt6
export PATH=/usr/lib64/qt6/bin:$PATH
%cmake  -DOGRE_PLUGIN_DIR=%{_libdir}/OGRE \
	-DUSE_SYSTEM_TINYXML=ON \
	-DOPENMW_USE_SYSTEM_BULLET=OFF \
 	-DOPENMW_USE_SYSTEM_RECASTNAVIGATION=ON \
	-DBUILD_UNITTESTS=OFF \
	-DUSE_QT=TRUE \
  	-DQT_MAJOR_VERSION=6 \
	-DMORROWIND_DATA_FILES=%{_datadir}/games/morrowind \
	-G Ninja

%ninja_build

%install
%ninja_install -C build

%files
%{_sysconfdir}/%{name}/
%{_bindir}/*
%{_datadir}/metainfo/openmw.appdata.xml
%{_gamesdatadir}/%{name}/
%{_datadir}/applications/*.desktop
%{_datadir}/pixmaps/%{name}.png
%{_datadir}/pixmaps/openmw-cs.png
