Name:		openmw
Version:	0.20.0
Release:	1
Summary:	A reimplementation of The Elder Scrolls III: Morrowind
Group:		Games/Adventure
License:	GPLv3
URL:		http://krank.sourceforge.net/
Source:		https://openmw.googlecode.com/files/%{name}_%{version}.orig.tar.bz2
BuildRequires:	cmake
BuildRequires:	boost-devel
BuildRequires:	qt4-devel
BuildRequires:	pkgconfig(bullet)
BuildRequires:	pkgconfig(libmpg123)
BuildRequires:	pkgconfig(MYGUI)
BuildRequires:	pkgconfig(OGRE)
BuildRequires:	pkgconfig(OIS)
BuildRequires:	pkgconfig(openal)
BuildRequires:	pkgconfig(sndfile)
# Looks like it's needed to build in "package" mode
BuildRequires:	dpkg

%description
OpenMW is an engine for 2002's game The Elder Scrolls 3: Morrowind.
It aims to be a fully playable (and improved!), open source
implementation of the game's engine and functionality.

You will still need the original game data to play OpenMW.

%prep
%setup -q

%build
%cmake
# Too greedy for resources
make

%install
%makeinstall_std -C build

%files
%{_sysconfdir}/%{name}
%{_gamesbindir}/%{name}
%{_gamesbindir}/omwlauncher
%{_gamesdatadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}.png

