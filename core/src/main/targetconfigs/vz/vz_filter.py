# Copyright (c) 2020, Oracle Corporation and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl.
#
# ------------
# Description:
# ------------
# This is a WDT filter for preparing a model for Verrazzano deployment.
# Remove partition, resource group elements.
# Remove machine, node manager, virtual target, migration elements


def filter_model(model):
    __cleanup_topology(model)
    __cleanup_resources(model)


def __cleanup_resources(model):
    if model and 'resources' in model:
        resources = model['resources']

        for delthis in ['PartitionWorkManager', 'Partition', 'ResourceGroup', 'ResourceGroupTemplate', 'VirtualHost',
                        'ResourceManager', 'ResourceManagement']:
            if resources.has_key(delthis):
                del resources[delthis]


def __cleanup_topology(model):
    if model and 'topology' in model:
        topology = model['topology']
        for delthis in ['NMProperties', 'VirtualTarget', 'Machine']:
            if topology.has_key(delthis):
                del topology[delthis]

        if topology.has_key('Cluster'):
            clusters = topology['Cluster']
            for cluster in clusters:
                for delthis in ['MigrationBasis', 'CandidateMachinesForMigratableServer', 'DatabaseLessLeasingBasis',
                                'ClusterMessagingMode']:
                    if clusters[cluster].has_key(delthis):
                        del clusters[cluster][delthis]

        if topology.has_key('Server'):
            servers = topology['Server']
            for server in servers:
                for delthis in ['Machine', 'CandidateMachine', 'AutoMigrationEnabled']:
                    if servers[server].has_key(delthis):
                        del servers[server][delthis]

        if topology.has_key('SecurityConfiguration'):
            for delthis in ['NodeManagerPasswordEncrypted', 'NodeManagerUsername']:
                if topology['SecurityConfiguration'].has_key(delthis):
                    del topology['SecurityConfiguration'][delthis]
            if len(topology['SecurityConfiguration'].keys()) == 0:
                del topology['SecurityConfiguration']

        if topology.has_key('ServerTemplate'):
            server_templates = topology['ServerTemplate']
            for server_template in server_templates:
                server_templates[server_template]['AutoMigrationEnabled'] = False
        else:
            topology['ServerTemplate'] = {}
            server_templates = topology['ServerTemplate']
            if topology.has_key('Cluster'):
                clusters = topology['Cluster']
                for cluster in clusters:
                    server_templates[cluster] = {}
                    server_template = server_templates[cluster]
                    server_template['Cluster'] = cluster
                    server_template['AutoMigrationEnabled'] = False