Summary:	A reimplementation of The Elder Scrolls III: Morrowind
Name:		openmw
Version:	0.24.0
Release:	1
Group:		Games/Adventure
License:	GPLv3
Url:		https://openmw.org
Source:		https://openmw.googlecode.com/files/%{name}-%{version}.tar.gz
BuildRequires:	cmake
BuildRequires:	ogre
BuildRequires:	boost-devel
BuildRequires:	ffmpeg-devel
BuildRequires:	qt4-devel
BuildRequires:	pkgconfig(bullet)
BuildRequires:	pkgconfig(libmpg123)
BuildRequires:	pkgconfig(MYGUI)
BuildRequires:	pkgconfig(OGRE)
BuildRequires:	pkgconfig(OIS)
BuildRequires:	pkgconfig(openal)
BuildRequires:	pkgconfig(sndfile)
BuildRequires:	pkgconfig(uuid)
# Looks like it's needed to build in "package" mode
BuildRequires:	dpkg
Requires:	ogre

%description
OpenMW is an engine for 2002's game The Elder Scrolls 3: Morrowind.
It aims to be a fully playable (and improved!), open source
implementation of the game's engine and functionality.

You will still need the original game data to play OpenMW.

%prep
%setup -q

%build
%cmake -DOGRE_PLUGIN_DIR=%{_libdir}/OGRE
# Too greedy for resources
make

%install
%makeinstall_std -C build

%files
%{_sysconfdir}/%{name}
%{_gamesbindir}/%{name}
%{_gamesbindir}/omwlauncher
%{_gamesbindir}/mwiniimport
%{_gamesdatadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}.png

