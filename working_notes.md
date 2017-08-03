# isoprene-pumpjack working notes

### Exmple/test data

#### Dolphins

https://networkdata.ics.uci.edu/data.php?id=6

An undirected social network of frequent associations between 62 dolphins in a community living off Doubtful Sound, New Zealand.

Original file `http://networkdata.ics.uci.edu/data/dolphins/dolphins.gml`

Converted to a JSON object in the style of:
```
{
  nodes: [
    { id: 'n0' },
    { id: 'n1' }
  ],
  edges: [
    {
      id: 'e0',
      source: 'n0',
      target: 'n1'
    }
  ]
}
```
