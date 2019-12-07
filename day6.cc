#include <bits/stdc++.h>

using namespace std;

typedef map<string, set<string> > graph;

int solve(graph& gf, string root) {
    set<string> visited;
    queue<pair<string, int> > q;
    q.push(make_pair(root, 0));
    visited.insert(root);
    int num_orbits = 0;
    while (!q.empty()) {
        pair<string, int> cur = q.front();
        q.pop();
        string node = cur.first;
        int depth = cur.second;
        num_orbits += depth;
        for (set<string>::iterator it = gf[node].begin(); it != gf[node].end(); ++it) {
            string nxt = *it;
            if (visited.find(nxt) != visited.end()) {
                continue;
            } else {
                q.push(make_pair(nxt, depth + 1));
            }
        }
        visited.insert(node);
    }
    return num_orbits;
}

int solveb(graph& gf, string src, string dst) {
    set<string> visited;
    queue<pair<string, int> > q;
    q.push(make_pair(src, 0));
    visited.insert(src);
    while (!q.empty()) {
        pair<string, int> cur = q.front();
        q.pop();
        string node = cur.first;
        int depth = cur.second;
        if (node == dst) {
            return depth;
        }
        for (set<string>::iterator it = gf[node].begin(); it != gf[node].end(); ++it) {
            string nxt = *it;
            if (visited.find(nxt) != visited.end()) {
                continue;
            } else {
                q.push(make_pair(nxt, depth + 1));
            }
        }
        visited.insert(node);
    }
    return -1;
}

int main() {
    string line;
    graph gf;

    string b_YOUsrc;
    string b_SANsrc;

    while(getline(cin, line)) {
        istringstream ls(line);
        string cur;
        string dst;
        getline(ls, cur, ')');
        getline(ls, dst);
        if (dst == "YOU") {
            b_YOUsrc = cur;
        } else if (dst == "SAN") {
            b_SANsrc = cur;
        }
        gf[cur].insert(dst);
        gf[dst].insert(cur);
    }
    cout << solve(gf, "COM") << endl;
    cout << solveb(gf, b_YOUsrc, b_SANsrc) << endl;
    return 0;
}
