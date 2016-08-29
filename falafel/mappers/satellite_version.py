import os
from falafel.core.plugins import mapper

foreman_sat61_ver_map = {
    '1.5': '6.0',
    '1.6.0.53': '6.0.8',
    '1.7': '6.1',
    '1.7.2.33': '6.1.1',
    '1.7.2.36': '6.1.2',
    '1.7.2.43': '6.1.3',
    '1.7.2.46': '6.1.4',
    '1.7.2.49': '6.1.5',
    '1.7.2.50': '6.1.6',
    '1.7.2.53': '6.1.7',
    '1.7.2.55': '6.1.8',
}


@mapper('satellite_version.rb')
@mapper('installed-rpms')
def get_sat_version(context):
    """
    Return the full version of Satellite 5.x and 6.x:
    - E.g.
      Satellite 5.x: "5.3.0.27-1.el5sat-noarch"
      Satellite 6.x: "6.0", "6.1.3" or "6.2.0.11-1.el7sat.noarch"
    ---
    For Satellite 6.x
    - https://access.redhat.com/articles/1343683
    - https://bugzilla.redhat.com/show_bug.cgi?id=1191584
    1. Check the version information in below files at first:
       - satellite_version
       - usr/share/foreman/lib/satellite/version.rb
    2. Check the version of foreman or satellite-installer, when the files
       listed in (1) are not found.
                            Sat 6.0     Sat 6.1     Sat 6.2
       foreman              1.5.x       1.7.x       1.11.0
       satellite-installer  -           -           6.2.x

    For Satellite 5.x
    - https://access.redhat.com/solutions/1224043
      Return the version of satellite-schema directly
      > 5.3~5.7: satellite-schema
      > 5.0~5.2: rhn-satellite-schema
      Because of satellite-branding is not deployed in Sat 5.0~5.2, and
      satellite-schema can also be used for checking the version, so here we use
      satellite-schema instead of satellite-branding
    """
    # For satellite_version
    if 'version' in os.path.basename(context.path).lower():
        for line in context.content:
            if line.strip().upper().startswith('VERSION'):
                return line.split()[-1].strip('"')
    # For installed-rpms
    else:
        sat5_pkg = ('satellite-schema-', 'rhn-satellite-schema-')
        sat61_pkg = 'foreman-1'  # Add "-1" to check the `foreman` package only
        # From Sat 6.2, we check `satellite-installer` instead of `foreman`
        sat62_pkg = 'satellite-installer-'
        for line in context.content:
            # for 6.0 and 6.1
            if line.startswith(sat61_pkg):
                pkg_ver = line.split('-')[1]
                sat61_ver = foreman_sat61_ver_map.get(pkg_ver)
                # for `1.5` and `1.7`
                sat61_ver = sat61_ver if sat61_ver else foreman_sat61_ver_map.get(pkg_ver[:3])
                if sat61_ver:
                    return sat61_ver
            # for 6.2, (`foreman-1.11.x` is ignored above)
            elif line.startswith(sat62_pkg):
                beg_idx = len(sat62_pkg)
                # return the version of `satellite-installer` directly
                return line.split()[0][beg_idx:]
            # for 5.x
            elif line.startswith(sat5_pkg):
                # return the version of `[rhn-]satellite-schema` directly
                pkg = line.split()[0]
                return pkg[pkg.find('schema-') + 7:]
    # Return None for no satellite installed
    return None
