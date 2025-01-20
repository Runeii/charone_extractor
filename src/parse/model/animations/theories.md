Here are the current theories based on MCH animation data analysis:

Header Structure (11 bytes)

Version Evolution
v2: Older format, uses 4-zero padding consistently
v4-6: Newer format, uses varying padding schemes (5/6/8/9 zeros)
Pattern complexity seems to increase with version number
Padding Info Theory
The padding_info value (4th header value) appears to determine the padding scheme
Positive values (0x04) = simpler 5/6 zero patterns
Negative values (0xf5ff, 0xd2ff) = more complex patterns
Could indicate compression method or data structure type
Block Structure
Most files show ~98 byte blocks between major padding markers
Block size might be related to data per bone or per frame
Later versions have more complex internal block structure
Common Patterns
All start with 5-zero padding at offset 11
Most have 4-zero padding early in the sequence
Regular spacing between padding blocks suggests structured frame or bone data
These patterns suggest this is a keyframe animation format that evolved to support more complex animations while maintaining backwards compatibility through the version system.


[2 bytes] Version (0x02-0x06) - Format version, seems to have evolved over time
[2 bytes] Format ID/Constant - Usually 0x01 but matches bone count in older versions
[2 bytes] Bone Count - Always matches model's bone count (0x17=23 or 0x32=50)
[2 bytes] Padding Info - Significant values seen: 0x04, 0xf5ff(-11), 0xd2ff(-46)
[2 bytes] Zero padding - Always 0x0000
[1 byte]  Frame Count - Values seen: 0xe8(232), 0xf0(240), 0x1f(31)

File 5 was an 'N' model
```markdown
| Feature | File 1 | File 2 | File 3 | File 4 | File 5 |
|---------|---------|---------|---------|---------|---------|
| Header | `05 00 01 00 17 00 f5 ff 00 00 e8` | `06 00 01 00 17 00 04 00 00 00 f0` | `04 00 01 00 17 00 04 00 00 00 f0` | `04 00 01 00 17 00 04 00 00 00 f0` | `02 00 32 00 32 00 d2 ff 00 00 1f` |
| Version | 5 | 6 | 4 | 4 | 2 |
| Constant | 1 | 1 | 1 | 1 | 50 (0x32) |
| Bones | 23 (0x17) | 23 (0x17) | 23 (0x17) | 23 (0x17) | 50 (0x32) |
| Padding Info | -11 (0xf5ff) | 4 | 4 | 4 | -46 (0xd2ff) |
| Frame Count? | 232 (0xe8) | 240 (0xf0) | 240 (0xf0) | 240 (0xf0) | 31 (0x1f) |
| Initial Pattern | 5-zero @ 11, 8-zero @ 96 | 5-zero @ 11, 4-zero @ 48 | 5-zero @ 11, 4-zero @ 48 | 5-zero @ 11, 4-zero @ 48 | Variable |
| Main Padding Pattern | 8/9 zeros | Mostly 5/6 zeros | Mostly 5/6 zeros | Mostly 5/6 zeros with some 4s | Only 4 zeros |
| Block Size | ~98 bytes | ~98 bytes | ~98 bytes | ~98 bytes | Variable |
```