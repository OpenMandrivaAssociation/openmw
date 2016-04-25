Summary:	A reimplementation of The Elder Scrolls III: Morrowind
Name:		openmw
Version:	0.39.0
Release:	2
Group:		Games/Adventure
License:	GPLv3+
Url:		https://openmw.org
Source0:	https://github.com/OpenMW/openmw/archive/%{name}-%{version}.tar.gz
Source1:	%{name}.rpmlintrc
BuildRequires:	cmake
BuildRequires:	ogre
BuildRequires:	boost-devel
BuildRequires:	ffmpeg-devel
BuildRequires:	qt4-devel
BuildRequires:	pkgconfig(bullet)
BuildRequires:	pkgconfig(openscenegraph)
BuildRequires:	pkgconfig(libmpg123)
BuildRequires:	pkgconfig(libunshield)
BuildRequires:	pkgconfig(MYGUI)
BuildRequires:	pkgconfig(OGRE)
BuildRequires:	pkgconfig(OIS)
BuildRequires:	pkgconfig(openal)
BuildRequires:	pkgconfig(sdl2)
BuildRequires:	pkgconfig(sndfile)
BuildRequires:	pkgconfig(uuid)
BuildRequires:	tinyxml-devel
Requires:	ogre

%description
OpenMW is an engine for 2002's game The Elder Scrolls 3: Morrowind.
It aims to be a fully playable (and improved!), open source
implementation of the game's engine and functionality.

You will still need the original game data to play OpenMW.

%prep
%setup -qn %{name}-%{name}-%{version}
%apply_patches

# Remove bundled tinyxml files
rm -f extern/oics/tiny*.

%build
%cmake_qt4 -DOGRE_PLUGIN_DIR=%{_libdir}/OGRE \
	-DUSE_SYSTEM_TINYXML=ON \
	-DBUILD_UNITTESTS=OFF \
	-DMORROWIND_DATA_FILES=%{_datadir}/games/morrowind

%make

%install
%makeinstall_std -C build

%files
%{_sysconfdir}/%{name}/
%{_bindir}/%{name}
%{_bindir}/openmw-cs
%{_bindir}/openmw-launcher
%{_bindir}/openmw-essimporter
%{_bindir}/openmw-wizard
%{_bindir}/esmtool
%{_bindir}/openmw-iniimporter
%{_bindir}/bsatool
%{_datadir}/appdata/openmw.appdata.xml
%{_gamesdatadir}/%{name}/
%{_datadir}/applications/%{name}.desktop
%{_datadir}/applications/openmw-cs.desktop
%{_datadir}/pixmaps/%{name}.png
%{_datadir}/pixmaps/openmw-cs.png
%{_datadir}/licenses/%{name}/
