#include <iostream>
#include <vector>
#include <set>
#include <string>
#include <queue>
#include <map>
#include <algorithm>

using namespace std;

struct Hexagon {
    int resource_id;   
    int activation_se; 
    int vertices[6];   
};

const int MAX_NODES = 54;
const int MAX_HEXES = 19;

struct Node {
    int id;
    int hex_count = 0;
    vector<int> adjacent_nodes; 
    bool has_dc = false;        
    int dc_level = 0;           
    int converter_type = -1; // -1: none, 0-4: specific, 5: 3-to-1
    int provides_mask = 0;   // Bitmask of resources (0-4) provided by adjacent hexes
    double yield_per_res[5] = {0, 0, 0, 0, 0};
    double yield_value = 0;
};

vector<Hexagon> map_hexes;
vector<Node> map_nodes;
long long resources[5];
// Tracking our infrastructure
vector<int> my_dcs;
set<int> network_nodes;
set<pair<int, int>> network_cables;

bool can_upgrade(int node_id, const long long resources[5]) {
    int target_level = map_nodes[node_id].dc_level + 1;
    return (resources[3] >= target_level && resources[4] >= (target_level + 1));
}

bool can_build_cable(const long long resources[5]) {
    return (resources[0] >= 1 && resources[1] >= 1);
}

bool can_build_dc(const long long resources[5]) {
    return (resources[0] >= 1 && resources[1] >= 1 && resources[2] >= 1 && resources[3] >= 1);
}

int get_best_conversion_rate(int resource_id) {
    bool has_31 = false;
    for (int dc_idx : my_dcs) {
        if (map_nodes[dc_idx].converter_type == resource_id) return 2;
        if (map_nodes[dc_idx].converter_type == 5) has_31 = true;
    }
    return has_31 ? 3 : 4;
}

// Găsește cel mai scurt drum de la rețea către o țintă
vector<int> find_path_to_node(int target, const set<int>& current_network) {
    if (target == -1 || current_network.count(target)) return {};
    
    queue<int> q;
    map<int, int> parent;
    for (int node : current_network) {
        q.push(node);
        parent[node] = -1;
    }

    int reached = -1;
    while (!q.empty()) {
        int curr = q.front(); q.pop();
        if (curr == target) { reached = curr; break; }
        for (int adj : map_nodes[curr].adjacent_nodes) {
            if (parent.find(adj) == parent.end()) {
                parent[adj] = curr;
                q.push(adj);
            }
        }
    }
    if (reached == -1) return {};
    vector<int> path;
    for (int v = reached; v != -1 && parent[v] != -1; v = parent[v]) path.push_back(v);
    reverse(path.begin(), path.end());
    return path; 
}

int main() {
    // Optimize standard I/O operations for speed
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int num_blueprints;
    if (!(cin >> num_blueprints)) {
        cerr << "CRASH: Failed to read number of blueprints!" << "\n";
        return 0; 
    }
    cerr << "DEBUG: Starting game with " << num_blueprints << " blueprints." << "\n";

    for (int b = 0; b < num_blueprints; ++b) {
        int Z; 
        if (!(cin >> Z)) break;
        cerr << "DEBUG: Blueprint " << b << " has " << Z << " days." << "\n";

        my_dcs.clear();
        network_nodes.clear();
        network_cables.clear();
        map_hexes.clear();
        map_hexes.resize(MAX_HEXES);
        map_nodes.clear();
        map_nodes.resize(MAX_NODES);
        for(int i = 0; i < MAX_NODES; ++i) map_nodes[i].id = i;
        
        // 1. Read Hexagons
        for (int i = 0; i < MAX_HEXES; ++i) {
            int res_id, se;
            cin >> res_id >> se;
            
            map_hexes.at(i).resource_id = res_id;
            map_hexes.at(i).activation_se = se;
            double weight = (se == 0) ? 0 : (6.0 - abs(7.0 - se));

            for (int v = 0; v < 6; ++v) {
                cin >> map_hexes.at(i).vertices[v];
                int node_id = map_hexes.at(i).vertices[v];
                map_nodes.at(node_id).yield_value += weight;
                if (res_id < 5) {
                    map_nodes.at(node_id).yield_per_res[res_id] += weight;
                    map_nodes.at(node_id).provides_mask |= (1 << res_id);
                }
            }
        }

        // 2. Read Converters
        for (int i = 0; i < 6; ++i) {
            string token;
            if (!(cin >> ws) || cin.peek() != 'C') break;
            if (cin >> token) {
                int count; if (!(cin >> count)) break;
                for (int j = 0; j < count; ++j) {
                    int node_id; if (!(cin >> node_id)) break;
                    if (node_id >= 0 && node_id < MAX_NODES) {
                        int c_val = stoi(token.substr(1));
                        if (c_val == 31) map_nodes.at(node_id).converter_type = 5;
                        else map_nodes.at(node_id).converter_type = c_val;
                    }
                }
            } else break;
        }

        // 3. Process edges
        set<pair<int, int>> unique_edges;
        for (int i = 0; i < MAX_HEXES; ++i) {
            for (int v = 0; v < 6; ++v) {
                int u = map_hexes[i].vertices[v];
                int w = map_hexes[i].vertices[(v + 1) % 6];
                unique_edges.insert({min(u, w), max(u, w)});
            }
        }
        
        for (const auto& edge : unique_edges) {
            int u = edge.first;
            int w = edge.second;
            map_nodes.at(u).adjacent_nodes.push_back(w);
            map_nodes.at(w).adjacent_nodes.push_back(u);
        }
        cerr << "DEBUG: Successfully processed edges. Sending initial commands..." << "\n";

        // 4. Select Initial Nodes based on Balanced Yield (Minimize Starvation)
        int dc1 = -1, dc2 = -1;
        double best_score = -1;

        for (int i = 0; i < MAX_NODES; ++i) {
            for (int j = i + 1; j < MAX_NODES; ++j) {
                bool is_adj = false;
                for (int neighbor : map_nodes[i].adjacent_nodes) {
                    if (neighbor == j) { is_adj = true; break; }
                }
                if (is_adj) continue;

                double pair_yield_res[4] = {0,0,0,0};
                double total_y = 0;
                for (int r = 0; r < 4; ++r) {
                    pair_yield_res[r] = map_nodes[i].yield_per_res[r] + map_nodes[j].yield_per_res[r];
                    total_y += pair_yield_res[r];
                }
                
                double min_y = pair_yield_res[0];
                for (int r = 1; r < 4; ++r) if (pair_yield_res[r] < min_y) min_y = pair_yield_res[r];

                // Scor echilibrat: Total + Bonus uriaș pentru resursa cea mai slabă
                double current_score = total_y + (min_y * 25.0);

                if (current_score > best_score) {
                    best_score = current_score;
                    dc1 = i;
                    dc2 = j;
                }
            }
        }
        if (dc1 == -1) { dc1 = 0; dc2 = 2; }
        
        // 5. Send Initial Construction Commands
        cout << "START" << endl;
        cout << "BUILD_DC " << dc1 << "\n";
        cout << "BUILD_DC " << dc2 << "\n";
        
        // Alegem vecinii care au yield-ul cel mai mare pentru a începe rețeaua
        auto get_best_neighbor = [&](int u) {
            int best_v = map_nodes[u].adjacent_nodes[0]; // Fallback
            double max_y = -1;
            for (int v : map_nodes[u].adjacent_nodes) {
                if (map_nodes[v].yield_value > max_y) {
                    max_y = map_nodes[v].yield_value;
                    best_v = v;
                }
            }
            return best_v;
        };

        int target1 = get_best_neighbor(dc1);
        int target2 = get_best_neighbor(dc2);

        cout << "BUILD_CABLE " << dc1 << " " << target1 << "\n";
        cout << "BUILD_CABLE " << dc2 << " " << target2 << "\n";

        map_nodes[dc1].has_dc = true;
        map_nodes[dc1].dc_level = 1; 
        my_dcs.push_back(dc1);
        network_nodes.insert(dc1);
        network_nodes.insert(target1);

        map_nodes[dc2].has_dc = true;
        map_nodes[dc2].dc_level = 1;
        my_dcs.push_back(dc2);
        network_nodes.insert(dc2);
        network_nodes.insert(target2);

        cout.flush();

        // 6. Daily Simulation Loop
        for (int day = 0; day < Z; ++day) {
            int current_se;

            if (!(cin >> current_se)) break;
            for(int i = 0; i < 5; ++i) cin >> resources[i];

            vector<string> daily_actions;

            bool made_progress = true;
            while (made_progress) {
                made_progress = false;

                // 0. Targeted Conversion: use abundant resources to unblock building
                for (int i = 0; i < 4; ++i) {
                    if (resources[i] == 0) {
                        for (int j = 0; j < 5; ++j) {
                            // Nu consumăm RAM (3) sau GPU (4) pentru a cumpăra resurse de bază (0, 1, 2)
                            if (i < 3 && j >= 3) continue;
                            int rate = get_best_conversion_rate(j);
                            if (resources[j] >= rate + 3) { // Buffer mai mare pentru a nu seca economia
                                daily_actions.push_back("CONVERT " + to_string(j) + " " + to_string(i));
                                resources[j] -= rate; resources[i]++;
                                made_progress = true; break;
                            }
                        }
                    }
                    if (made_progress) break;
                }
                if (made_progress) continue;

                // Determinăm ordinea priorității (RAM vs GPU) în funcție de nevoile primului upgrade disponibil
                vector<int> targets = {3, 4};
                int candidate_dc = -1;
                for (int node_id : my_dcs) {
                    if (map_nodes[node_id].dc_level < 3) {
                        if (candidate_dc == -1 || map_nodes[node_id].dc_level < map_nodes[candidate_dc].dc_level)
                            candidate_dc = node_id;
                    }
                }
                if (candidate_dc != -1) {
                    int ram_req = map_nodes[candidate_dc].dc_level + 1;
                    int gpu_req = ram_req + 1;
                    if ((gpu_req - resources[4]) > (ram_req - resources[3])) targets = {4, 3};
                }

                // Conversie agresivă pentru GPU/RAM
                for (int target_res : targets) { 
                    if (resources[target_res] < 5) {
                        for (int j = 0; j < 3; ++j) { // Din Energy, Water sau Data
                            if (j == 2 && resources[j] <= 1) continue; // Protejăm Data pentru BUILD_DC
                            int rate = get_best_conversion_rate(j);
                            if (resources[j] >= 15) {
                                daily_actions.push_back("CONVERT " + to_string(j) + " " + to_string(target_res));
                                resources[j] -= rate; resources[target_res]++;
                                made_progress = true; break;
                            }
                        }
                    }
                    if (made_progress) break;
                }
                if (made_progress) continue;

                // 1. Try to build a new DC if a network node is available and valid
                int best_dc_candidate = -1;
                double best_dc_candidate_yield = -1;

                for (int candidate_node_id : network_nodes) {
                    if (!map_nodes[candidate_node_id].has_dc && can_build_dc(resources)) {
                        // Verify Distance Rule
                        bool dist_ok = true;
                        for (int adj : map_nodes[candidate_node_id].adjacent_nodes) {
                            if (map_nodes[adj].has_dc) { dist_ok = false; break; }
                        }
                        
                        if (dist_ok) {
                            if (map_nodes[candidate_node_id].yield_value > best_dc_candidate_yield) {
                                best_dc_candidate_yield = map_nodes[candidate_node_id].yield_value;
                                best_dc_candidate = candidate_node_id;
                            }
                        }
                    }
                }

                if (best_dc_candidate != -1) {
                    daily_actions.push_back("BUILD_DC " + to_string(best_dc_candidate));
                    resources[0] -= 1; resources[1] -= 1; resources[2] -= 1; resources[3] -= 1;
                    map_nodes[best_dc_candidate].has_dc = true;
                    map_nodes[best_dc_candidate].dc_level = 1;
                    my_dcs.push_back(best_dc_candidate);
                    made_progress = true;
                }
                if (made_progress) continue; 

                // 2. Upgrade existing DCs (Higher ROI)
                vector<int> dcs_to_upgrade = my_dcs;
                sort(dcs_to_upgrade.begin(), dcs_to_upgrade.end(), [](int a, int b) {
                    if (map_nodes[a].dc_level != map_nodes[b].dc_level)
                        return map_nodes[a].dc_level < map_nodes[b].dc_level;
                    return map_nodes[a].yield_value > map_nodes[b].yield_value;
                });

                for (int node_id : dcs_to_upgrade) {
                    int target_level = map_nodes[node_id].dc_level + 1;
                    if (can_upgrade(node_id, resources) && target_level <= 3) {
                        
                        // Verificăm dacă există un nod cu convertor disponibil în rețea pentru BUILD_DC
                        bool converter_site_available = false;
                        for (int v : network_nodes) {
                            if (!map_nodes[v].has_dc && map_nodes[v].converter_type != -1) {
                                bool dist_ok = true;
                                for (int adj : map_nodes[v].adjacent_nodes)
                                    if (map_nodes[adj].has_dc) { dist_ok = false; break; }
                                if (dist_ok) { converter_site_available = true; break; }
                            }
                        }

                        // Dacă avem un loc de convertor, nu facem upgrade dacă RAM-ul rămas ar fi < 1
                        if (converter_site_available && (resources[3] - target_level < 1)) continue;

                        daily_actions.push_back("UPGRADE_DC " + to_string(node_id));
                        resources[3] -= target_level;
                        resources[4] -= (target_level + 1);
                        map_nodes[node_id].dc_level++;
                        made_progress = true;
                        break;
                    }
                }
                if (made_progress) continue;

                // 3. Try to expand network with cables
                // Optimizare ROI: Oprim expansiunea în ultimele 10 zile
                if (day < Z - 10 && can_build_cable(resources) && network_nodes.size() < MAX_NODES) {
                    int best_target = -1;
                    vector<int> best_path;
                    double best_roi = -1;

                    for (int i = 0; i < MAX_NODES; ++i) {
                        if (network_nodes.count(i)) continue;
                        bool possible_dc = true;
                        for (int adj : map_nodes[i].adjacent_nodes) if (map_nodes[adj].has_dc) possible_dc = false;

                        if (possible_dc) {
                            vector<int> path = find_path_to_node(i, network_nodes);
                            if (!path.empty()) {
                                // ROI: (Yield + Bonus Converter) / Distanta
                                double potential = map_nodes[i].yield_value + (map_nodes[i].converter_type == 5 ? 10.0 : 0.0);
                                double roi = potential / (double)path.size();
                                if (roi > best_roi) {
                                    best_roi = roi;
                                    best_target = i;
                                    best_path = path;
                                }
                            }
                        }
                    }

                    if (!best_path.empty()) {
                        int next_node = best_path[0];
                        // Găsim nodul din rețea care se conectează la next_node
                        for (int u : network_nodes) {
                            for (int v : map_nodes[u].adjacent_nodes) {
                                if (v == next_node) {
                                    daily_actions.push_back("BUILD_CABLE " + to_string(u) + " " + to_string(v));
                                    resources[0] -= 1; resources[1] -= 1;
                                    network_nodes.insert(v);
                                    made_progress = true; break;
                                }
                            }
                            if (made_progress) break;
                        }
                    }
                }
                if (made_progress) continue;
            }

            // Send all actions for the day
            cout << daily_actions.size() << "\n";
            for (const string& cmd : daily_actions) {
                cout << cmd << "\n";
            }
            cout.flush();
        }
    }
    return 0;
}//2305