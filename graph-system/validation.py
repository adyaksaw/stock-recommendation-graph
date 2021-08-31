import networkx as nx


def write_to_file(lines, filename):
    with open(f"warning/{filename}", 'w') as file:
        file.write("\n".join(lines))


class Validation:
    def validate_to_file(graph: nx.graph):
        write_to_file(Validation.validate_sp001(graph), 'sp001.txt')
        write_to_file(Validation.validate_sp002(graph), 'sp002.txt')
        write_to_file(Validation.validate_dp001(graph), 'dp001.txt')
        write_to_file(Validation.validate_dp002(graph), 'dp002.txt')
        write_to_file(Validation.validate_dk001(graph), 'dk001.txt')
        write_to_file(Validation.validate_dk002(graph), 'dk002.txt')
        write_to_file(Validation.validate_dk003_dk004(
            graph), 'dk003_dk004.txt')
        write_to_file(Validation.validate_dk005(graph), 'dk005.txt')
        write_to_file(Validation.validate_ka001(graph), 'ka001.txt')
        write_to_file(Validation.validate_ka002(graph), 'ka002.txt')

    def validate(graph: nx.graph):
        warning = []
        warning += Validation.validate_sp001(graph)
        warning += Validation.validate_sp002(graph)
        warning += Validation.validate_dp001(graph)
        warning += Validation.validate_dp001(graph)
        warning += Validation.validate_dp002(graph)
        warning += Validation.validate_dk001(graph)
        warning += Validation.validate_dk002(graph)
        warning += Validation.validate_dk003_dk004(graph)
        warning += Validation.validate_dk005(graph)
        warning += Validation.validate_ka001(graph)
        warning += Validation.validate_ka002(graph)
        return warning

    def validate_sp001(graph: nx.Graph):
        warning = []
        for node, node_attr in graph.nodes(data=True):
            if node_attr['entity_type'] == 'perusahaan tercatat':
                sekretaris_count = 0
                for _, _, edge_attr in graph.edges(node, data=True):
                    if edge_attr['relation_type'] == 'sekretaris perusahaan':
                        sekretaris_count += 1
                if sekretaris_count == 0:
                    warning.append(
                        f"sp001: {node} - 0 sekretaris found | expected > 0")
        return warning

    def validate_sp002(graph: nx.Graph):
        warning = []
        for node, node_attr in graph.nodes(data=True):
            if node_attr['entity_type'] == 'entitas lain':
                sekretaris_count = 0
                other_count = 0
                val = ''
                for _, _, edge_attr in graph.edges(node, data=True):
                    if edge_attr['relation_type'] == 'sekretaris perusahaan':
                        sekretaris_count += 1
                    elif edge_attr['relation_type'] != 'direktur' and edge_attr['relation_type'] != 'pemegang saham':
                        other_count += 1
                        val = edge_attr['relation_type']
                if sekretaris_count > 0 and other_count > 0:
                    warning.append(
                        f"sp002: {node} - {other_count} jabatan found, one of them is {val} | expected no overlap with sekretaris perusahaan")
        return warning

    def validate_dp001(graph: nx.Graph):
        warning = []
        for node, node_attr in graph.nodes(data=True):
            if node_attr['entity_type'] == 'perusahaan tercatat':
                direktur_count = 0
                for _, _, edge_attr in graph.edges(node, data=True):
                    if edge_attr['relation_type'] == 'direktur':
                        direktur_count += 1
                if direktur_count < 2:
                    warning.append(
                        f"dp001: {node} - {direktur_count} direktur in the company | expected >= 2")
        return warning

    def validate_dp002(graph: nx.Graph):
        warning = []
        for node, node_attr in graph.nodes(data=True):
            if node_attr['entity_type'] == 'entitas lain':
                direktur_count = 0
                komisaris_count = 0
                komite_count = 0
                for _, _, edge_attr in graph.edges(node, data=True):
                    if edge_attr['relation_type'] == 'direktur':
                        direktur_count += 1
                    elif edge_attr['relation_type'] == 'komisaris':
                        komisaris_count += 1
                    elif edge_attr['relation_type'] == 'komite audit':
                        komite_count += 1
                if direktur_count > 2 or komisaris_count > 3 or komite_count > 5:
                    warning.append(
                        f"dp002: {node} - {direktur_count} direktur, {komisaris_count} komisaris, {komite_count} komite audit| expected direktur <= 2 and komisaris <= 3 and komite <= 5")
        return warning

    def validate_dk001(graph: nx.Graph):
        warning = []
        for node, node_attr in graph.nodes(data=True):
            if node_attr['entity_type'] == 'perusahaan tercatat':
                komisaris_count = 0
                for _, _, edge_attr in graph.edges(node, data=True):
                    if edge_attr['relation_type'] == 'komisaris':
                        komisaris_count += 1
                if komisaris_count < 2:
                    warning.append(
                        f"dk001: {node} - {komisaris_count} komisaris | expected komisaris >= 2")
        return warning

    def validate_dk002(graph: nx.Graph):
        warning = []
        for node, node_attr in graph.nodes(data=True):
            if node_attr['entity_type'] == 'perusahaan tercatat':
                komisaris_count = 0
                komisaris_independen_count = 0
                for _, _, edge_attr in graph.edges(node, data=True):
                    if edge_attr['relation_type'] == 'komisaris':
                        komisaris_count += 1
                    if edge_attr['subrelation_type'] == 'komisaris independen':
                        komisaris_independen_count += 1
                if komisaris_count == 2 and komisaris_independen_count != 1:
                    warning.append(f"dk002: {node}")
                elif komisaris_count > 2 and komisaris_count * 0.3 > komisaris_independen_count:
                    warning.append(f"dk002: {node}")
        return warning

    def validate_dk003_dk004(graph: nx.Graph):
        warning = []
        for node, node_attr in graph.nodes(data=True):
            if node_attr['entity_type'] == 'entitas lain':
                direktur_count = 0
                komisaris_count = 0
                for _, _, edge_attr in graph.edges(node, data=True):
                    if edge_attr['relation_type'] == 'direktur':
                        direktur_count += 1
                    elif edge_attr['relation_type'] == 'komisaris':
                        komisaris_count += 1
                if direktur_count > 2 or (komisaris_count > 3 and direktur_count > 0):
                    warning.append(
                        f"dk003: {node} - {direktur_count} direktur dan {komisaris_count} komisaris | expected direktur <= 2 or (komisaris <= 3 or direktur == 0)")
                elif komisaris_count > 5:
                    warning.append(
                        f"dk004: {node} - {komisaris_count} komisaris | expected komisaris <= 5")
        return warning

    def validate_dk005(graph: nx.Graph):
        warning = []
        for node, node_attr in graph.nodes(data=True):
            if node_attr['entity_type'] == 'entitas lain':
                komite_set = set()
                jabatan_set = set()
                komisaris_count = 0
                for u, v, edge_attr in graph.edges(node, data=True):
                    if edge_attr['relation_type'] == 'komite audit':
                        if u == node:
                            komite_set.add(v)
                        else:
                            komite_set.add(u)
                    if edge_attr['relation_type'] == 'direktur' or edge_attr['relation_type'] == 'komisaris':
                        if u == node:
                            jabatan_set.add(v)
                        else:
                            jabatan_set.add(u)
                    if edge_attr['relation_type'] == 'komisaris':
                        komisaris_count += 1

                if len(komite_set.intersection(jabatan_set)) > 5:
                    warning.append(
                        f"dk005: {node} - {len(komite_set.intersection(jabatan_set))} komite audit rangkap jabatan")
        return warning

    def validate_ka001(graph: nx.Graph):
        warning = []
        for node, node_attr in graph.nodes(data=True):
            if node_attr['entity_type'] == 'perusahaan tercatat':
                komite_count = 0
                for _, _, edge_attr in graph.edges(node, data=True):
                    if edge_attr['relation_type'] == 'komite audit':
                        komite_count += 1
                if komite_count < 3:
                    warning.append(
                        f"ka001: {node} - {komite_count} komite audit | expected komite >= 3")
        return warning

    def validate_ka002(graph: nx.Graph):
        warning = []
        for node, node_attr in graph.nodes(data=True):
            if node_attr['entity_type'] == 'entitas lain':
                komite_set = set()
                pemegang_saham_set = set()
                for u, v, edge_attr in graph.edges(node, data=True):
                    if edge_attr['relation_type'] == 'komite audit':
                        if u == node:
                            komite_set.add(v)
                        else:
                            komite_set.add(u)
                    if edge_attr['relation_type'] == 'pemegang saham':
                        if u == node:
                            pemegang_saham_set.add(v)
                        else:
                            pemegang_saham_set.add(u)
                if len(komite_set.intersection(pemegang_saham_set)) > 0:
                    warning.append(
                        f"ka002: {node} - {len(komite_set.intersection(pemegang_saham_set))} komite audit rangkap pemegang saham")
        return warning
