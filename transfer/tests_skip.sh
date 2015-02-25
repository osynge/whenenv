cat <<'EOF' > tests.xml
<?xml version="1.0" encoding="utf-8"?>
<testsuites errors="0" failures="0" tests="1" time="45">
    <testsuite errors="0" failures="0" hostname="localhost" id="0" name="base_test_1" package="testdb" tests="1" timestamp="2012-11-15T01:02:29">
        <testcase classname="test.dummy" name="001-passed-test" time="1"/>
    </testsuite>
</testsuites>
EOF
cat tests.xml
