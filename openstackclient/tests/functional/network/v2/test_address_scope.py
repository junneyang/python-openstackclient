#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import re
import uuid

from openstackclient.tests.functional import base


class AddressScopeTests(base.TestCase):
    """Functional tests for address scope. """

    # NOTE(dtroyer): Do not normalize the setup and teardown of the resource
    #                creation and deletion.  Little is gained when each test
    #                has its own needs and there are collisions when running
    #                tests in parallel.

    @classmethod
    def setUpClass(cls):
        # Set up some regex for matching below
        cls.re_name = re.compile("name\s+\|\s+([^|]+?)\s+\|")
        cls.re_ip_version = re.compile("ip_version\s+\|\s+(\S+)")
        cls.re_shared = re.compile("shared\s+\|\s+(\S+)")

    def test_address_scope_delete(self):
        """Test create, delete multiple"""
        name1 = uuid.uuid4().hex
        raw_output = self.openstack(
            'address scope create ' + name1,
        )
        self.assertEqual(
            name1,
            re.search(self.re_name, raw_output).group(1),
        )
        # Check the default values
        self.assertEqual(
            'False',
            re.search(self.re_shared, raw_output).group(1),
        )

        name2 = uuid.uuid4().hex
        raw_output = self.openstack(
            'address scope create ' + name2,
        )
        self.assertEqual(
            name2,
            re.search(self.re_name, raw_output).group(1),
        )

        raw_output = self.openstack(
            'address scope delete ' + name1 + ' ' + name2,
        )
        self.assertOutput('', raw_output)

    def test_address_scope_list(self):
        """Test create defaults, list filters, delete"""
        name1 = uuid.uuid4().hex
        raw_output = self.openstack(
            'address scope create --ip-version 4 --share ' + name1,
        )
        self.addCleanup(self.openstack, 'address scope delete ' + name1)
        self.assertEqual(
            '4',
            re.search(self.re_ip_version, raw_output).group(1),
        )
        self.assertEqual(
            'True',
            re.search(self.re_shared, raw_output).group(1),
        )

        name2 = uuid.uuid4().hex
        raw_output = self.openstack(
            'address scope create --ip-version 6 --no-share ' + name2,
        )
        self.addCleanup(self.openstack, 'address scope delete ' + name2)
        self.assertEqual(
            '6',
            re.search(self.re_ip_version, raw_output).group(1),
        )
        self.assertEqual(
            'False',
            re.search(self.re_shared, raw_output).group(1),
        )

        # Test list
        raw_output = self.openstack('address scope list')
        self.assertIsNotNone(re.search(name1 + "\s+\|\s+4", raw_output))
        self.assertIsNotNone(re.search(name2 + "\s+\|\s+6", raw_output))

        # Test list --share
        # TODO(dtroyer): returns 'HttpException: Bad Request'
        # raw_output = self.openstack('address scope list --share')
        # self.assertIsNotNone(re.search(name1 + "\s+\|\s+4", raw_output))
        # self.assertIsNotNone(re.search(name2 + "\s+\|\s+6", raw_output))

        # Test list --no-share
        # TODO(dtroyer): returns 'HttpException: Bad Request'
        # raw_output = self.openstack('address scope list --no-share')
        # self.assertIsNotNone(re.search(name1 + "\s+\|\s+4", raw_output))
        # self.assertIsNotNone(re.search(name2 + "\s+\|\s+6", raw_output))

    def test_address_scope_set(self):
        """Tests create options, set, show, delete"""
        name = uuid.uuid4().hex
        newname = name + "_"
        raw_output = self.openstack(
            'address scope create ' +
            '--ip-version 4 ' +
            '--no-share ' +
            name,
        )
        self.addCleanup(self.openstack, 'address scope delete ' + newname)
        self.assertEqual(
            name,
            re.search(self.re_name, raw_output).group(1),
        )
        self.assertEqual(
            '4',
            re.search(self.re_ip_version, raw_output).group(1),
        )
        self.assertEqual(
            'False',
            re.search(self.re_shared, raw_output).group(1),
        )

        raw_output = self.openstack(
            'address scope set ' +
            '--name ' + newname +
            ' --share ' +
            name,
        )
        self.assertOutput('', raw_output)

        raw_output = self.openstack('address scope show ' + newname)
        self.assertEqual(
            newname,
            re.search(self.re_name, raw_output).group(1),
        )
        self.assertEqual(
            '4',
            re.search(self.re_ip_version, raw_output).group(1),
        )
        self.assertEqual(
            'True',
            re.search(self.re_shared, raw_output).group(1),
        )