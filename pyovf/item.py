#!/usr/bin/python
#
# Copyright (c) SAS Institute Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


from pyovf import ovf

class Cpu(ovf.Item):
    rasd_Caption = 'Virtual CPU'
    rasd_Description = 'Number of virtual CPUs'
    rasd_ElementName = 'some virt cpu'
    rasd_InstanceID = '1'
    rasd_ResourceType = '3'
    rasd_VirtualQuantity = '1'

class Memory(ovf.Item):
    rasd_AllocationUnits = 'MegaBytes'
    rasd_Caption = '256 MB of memory'
    rasd_Description = 'Memory Size'
    rasd_ElementName = 'some mem size'
    rasd_InstanceID = '2'
    rasd_ResourceType = '4'
    rasd_VirtualQuantity = '256'

class Harddisk(ovf.Item):
    rasd_Caption = 'Harddisk'
    rasd_ElementName = 'Hard disk'
    rasd_HostResource = 'ovf://disk/disk_1'
    rasd_InstanceID = '5'
    rasd_Parent = '4'
    rasd_ResourceType = '17'

class ScsiController(ovf.Item):
    rasd_Caption = 'SCSI Controller 0 - LSI Logic'
    rasd_ElementName = 'LSILOGIC'
    rasd_InstanceID = '4'
    rasd_ResourceSubType = 'LsiLogic'
    rasd_ResourceType = '6'
